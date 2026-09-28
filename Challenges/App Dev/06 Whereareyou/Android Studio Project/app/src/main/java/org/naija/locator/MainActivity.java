package org.naija.locator;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

/** Plain launcher stub - the real logic lives in {@link LocationService}. */
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        tv.setText("Locator ready");
        setContentView(tv);
    }
}
