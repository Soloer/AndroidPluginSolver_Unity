package com.gmrz.asm.test;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

import com.gmrz.asm.lib3.Lib_3_SDK;
import com.gmrz.asm.lib_1.Lib_1_SDK;
import com.gmrz.asm.lib_2.Lib_2_SDK;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Lib_1_SDK.get();
        Lib_2_SDK.get();
        Lib_3_SDK.get();
    }
}
