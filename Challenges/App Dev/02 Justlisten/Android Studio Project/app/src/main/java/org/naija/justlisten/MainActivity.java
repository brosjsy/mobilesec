package org.naija.justlisten;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;

/**
 * Challenge 2: Justlisten.
 *
 * The flag is announced system-wide with a broadcast Intent, action
 * "com.mobisec.intent.action.FLAG_ANNOUNCEMENT", carrying the flag under the
 * "flag" key in its extras Bundle.
 *
 * The catch (per the challenge's own hint): since Android 8.0 (API 26), the
 * OS ignores manifest-declared <receiver> entries for most implicit
 * broadcasts, regardless of the receiving app's own targetSdkVersion -- it's
 * a device/OS-level restriction, not something our manifest can opt out of.
 * A receiver registered at RUNTIME via Context.registerReceiver(), however,
 * is exempt from that restriction and still gets every matching broadcast.
 * So instead of declaring a <receiver> in AndroidManifest.xml, we register
 * one dynamically here in onCreate() -- this works correctly on every
 * Android version, old or new.
 */
public class MainActivity extends Activity {

    private static final String TAG = "MOBISEC";
    private static final String ACTION_FLAG =
            "com.mobisec.intent.action.FLAG_ANNOUNCEMENT";

    private final BroadcastReceiver flagReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String flag = intent.getStringExtra("flag");
            Log.i(TAG, "received FLAG_ANNOUNCEMENT broadcast");
            Log.i(TAG, "flag: " + flag);

            // Defensive: in case the flag isn't a plain String extra, dump
            // every extra key/value so nothing is missed.
            Bundle extras = intent.getExtras();
            if (extras != null) {
                for (String key : extras.keySet()) {
                    Log.i(TAG, "extra[" + key + "] = " + extras.get(key));
                }
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        IntentFilter filter = new IntentFilter(ACTION_FLAG);
        // RECEIVER_EXPORTED is required on API 33+ for a dynamically
        // registered receiver of a broadcast sent by another app/process;
        // the flag constant doesn't exist before API 33, so we branch.
        if (android.os.Build.VERSION.SDK_INT >= 33) {
            registerReceiver(flagReceiver, filter, Context.RECEIVER_EXPORTED);
        } else {
            registerReceiver(flagReceiver, filter);
        }
        Log.i(TAG, "listening for " + ACTION_FLAG);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(flagReceiver);
    }
}
