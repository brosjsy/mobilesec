package org.naija.helloworld;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

/**
 * Challenge 1: Helloworld.
 *
 * Requirement: print the exact string "hello-world-mobisec-edition" to the
 * system log, tagged "MOBISEC", so the grading harness's logcat scrape
 * picks it up. Confirms the toolchain (build, install, launch, Log.i)
 * works end to end.
 */
public class MainActivity extends Activity {

    private static final String TAG = "MOBISEC";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.i(TAG, "hello-world-mobisec-edition");
    }
}
