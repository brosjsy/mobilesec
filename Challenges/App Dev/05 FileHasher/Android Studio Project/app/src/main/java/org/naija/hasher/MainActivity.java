package org.naija.hasher;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

/**
 * Challenge 01: FileHasher.
 *
 * Plain launcher activity - required only so the app has a MAIN/LAUNCHER
 * entry point and can be installed/launched normally (the original build
 * failed with "Failed to find main activity" until this was added). The
 * actual challenge logic lives in {@link HashActivity}, which is the
 * exported component that does the real work.
 */
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        tv.setText("Hasher ready");
        setContentView(tv);
    }
}
