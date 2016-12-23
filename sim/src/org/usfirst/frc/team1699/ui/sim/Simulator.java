package org.usfirst.frc.team1699.ui.sim;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Orientation;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import org.usfirst.frc.team1699.utils.inireader.ConfigFile;
import org.usfirst.frc.team1699.utils.inireader.ConfigLine;
import org.usfirst.frc.team1699.utils.inireader.ConfigSection;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class Simulator extends Application {

    private String output = "";
    private List<String> args;
    private ConfigFile cf = null;
    private List<ConfigSection> sections = null;

    @Override
    public void init() throws Exception {
        this.args = this.getParameters().getRaw();
        if (this.args.size() == 1) {
            File config = new File(this.args.get(0)); // get the file parameter
            this.cf = new ConfigFile(config);

            ConfigSection cs;
            int i = 0;
            this.sections = new ArrayList<>();
            while ((cs = cf.getSection(i)) != null) {
                sections.add(cs);
                i += 1;
            }
        }

    }

    @Override
    public void start(Stage stage) throws Exception {
        if (this.args.size() != 1) {
            Alert a = new Alert(Alert.AlertType.ERROR);
            a.setTitle("ini-reader Simulation");
            a.setHeaderText("Error with command line arguments");
            a.setContentText("The usage of this program is: \nSimulator config-file");
            a.showAndWait();
            System.exit(1);
        }

        ScrollPane scroll = new ScrollPane();
        VBox box = new VBox();
        scroll.setContent(box);

        TitledPane titled;
        for (ConfigSection cs : sections) {

            ListView<ConfigLine<?>> lv = new ListView<>();

            ObservableList<ConfigLine<?>> ol = FXCollections.observableArrayList(cs.getLines());
            lv.setItems(ol);
            lv.setEditable(false);
            lv.setPrefHeight(cs.getLines().size() * 24);
            lv.setOrientation(Orientation.VERTICAL);

            titled = new TitledPane("ConfigSection " + cs.getName(), lv);
            titled.setExpanded(false);
            box.getChildren().add(titled);
        }

        ((TitledPane) box.getChildren().get(0)).setExpanded(true);

        stage.setScene(new Scene(scroll));
        stage.setTitle("ini-reader Simulator");
        stage.show();
    }

    public static void main(String[] args) {
        Application.launch(args);
    }


}
