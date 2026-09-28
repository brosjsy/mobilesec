package org.naija.locator;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;

import java.util.List;

/**
 * Challenge 02: Whereareyou.
 *
 * Vulnerable location service: on start it looks up the most recent cached
 * fix across every location provider and broadcasts it via a plain
 * sendBroadcast() with a public, unprotected action string
 * ("com.mobisec.intent.action.LOCATION_ANNOUNCEMENT") and no
 * android:permission requirement. Any other app on the device - not just an
 * intended companion app - can register a BroadcastReceiver for that same
 * action and read the "location" extra straight out of the air, with zero
 * IPC authentication. This class is the target/vulnerable side; exploitation
 * is simply registering a receiver for ACTION_ANNOUNCE and starting this
 * service (or waiting for it to run).
 */
public class LocationService extends Service {
    private static final String TAG = "LocationService";
    private static final String ACTION_ANNOUNCE = "com.mobisec.intent.action.LOCATION_ANNOUNCEMENT";

    private LocationManager lm;
    private boolean pending = false;

    private final LocationListener listener = new LocationListener() {
        @Override
        public void onLocationChanged(Location loc) {
            // Only answer here if a request found no location cached yet.
            if (pending) {
                pending = false;
                announce(loc);
            }
        }

        @Override public void onStatusChanged(String p, int s, Bundle e) {}
        @Override public void onProviderEnabled(String p) {}
        @Override public void onProviderDisabled(String p) {}
    };

    @Override
    public void onCreate() {
        super.onCreate();
        lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        try {
            // Keep every provider active so the cached fix stays current.
            for (String p : lm.getAllProviders()) {
                lm.requestLocationUpdates(p, 0, 0, listener);
            }
        } catch (SecurityException e) {
            Log.e(TAG, "no location permission", e);
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Location best = getCurrentLocation();
        if (best != null) {
            announce(best);
        } else {
            pending = true;
        }
        return START_NOT_STICKY;
    }

    /** Most recent fix across all providers. */
    private Location getCurrentLocation() {
        Location best = null;
        try {
            List<String> providers = lm.getAllProviders();
            for (String p : providers) {
                Location l = lm.getLastKnownLocation(p);
                if (l != null && (best == null || l.getTime() > best.getTime())) {
                    best = l;
                }
            }
        } catch (SecurityException e) {
            Log.e(TAG, "no location permission", e);
        }
        return best;
    }

    private void announce(Location loc) {
        Intent i = new Intent();
        i.setAction(ACTION_ANNOUNCE);
        i.putExtra("location", loc);
        sendBroadcast(i);
    }

    @Override
    public void onDestroy() {
        try {
            lm.removeUpdates(listener);
        } catch (SecurityException ignored) {
        }
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
