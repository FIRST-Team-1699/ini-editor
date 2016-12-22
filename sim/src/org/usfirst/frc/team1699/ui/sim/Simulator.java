package org.usfirst.frc.team1699.ui.sim;

import org.usfirst.frc.team1699.utils.inireader.ConfigFile;
import org.usfirst.frc.team1699.utils.inireader.ConfigSection;

import java.io.File;

public class Simulator {

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Usage: Simulator.jar config");
            System.exit(1);
        }
        File config = new File(args[0]);
        ConfigFile cf = new ConfigFile(config);

        int i = 0;
        ConfigSection cs;
        while ((cs = cf.getSection(i)) != null) {
            System.out.println(cs.toString());
            i += 1;
        }
    }
}
