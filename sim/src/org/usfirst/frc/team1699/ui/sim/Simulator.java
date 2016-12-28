/**
 *
 */
package org.usfirst.frc.team1699.ui.sim;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Orientation;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.ListView;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.TitledPane;
import javafx.scene.image.Image;
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
        // Check for args size, raise error if not 1
        if (this.args.size() != 1) {
            Alert a = new Alert(Alert.AlertType.ERROR);
            a.setTitle("ini-reader Simulation");
            a.setHeaderText("Error with command line arguments");
            a.setContentText("The usage of this program is: \nSimulator config-file");
            a.showAndWait();
            System.exit(1);
        }

        // Make a ScrollPane to make the box scrollable
        ScrollPane scroll = new ScrollPane();

        // Make a VBox to store everything
        VBox box = new VBox();
        scroll.setContent(box);

        int sum = 0;
        List<String> config_out;
        TitledPane titled;


        for (ConfigSection cs : sections) {

            config_out = new ArrayList<>();

            for (ConfigLine<?> cl : cs.getLines()) {
                if (cl.getName().trim().equals("")) {
                    config_out.add("ConfigLine<" + cl.getRawValue().getClass().getSimpleName() + "> "
                            + cl.getRawValue().toString());
                } else {
                    config_out.add("ConfigLine<" + cl.getRawValue().getClass().getSimpleName() + "> " + cl.getName() +
                            " = " + cl.getRawValue().toString());
                }
            }

            ListView<String> lv = new ListView<>();
            ObservableList<String> ol = FXCollections.observableArrayList(config_out);
            lv.setItems(ol);
            lv.setEditable(false);
            lv.setPrefHeight(cs.getLines().size() * 23);
            lv.setOrientation(Orientation.VERTICAL);

            sum += cs.getLines().size() + 2;

            titled = new TitledPane("ConfigSection " + cs.getName(), lv);
            titled.setExpanded(false);
            box.getChildren().add(titled);
        }

        ((TitledPane) box.getChildren().get(0)).setExpanded(true);

        BorderPane bp = new BorderPane();
        bp.setCenter(scroll);

        scroll.setVbarPolicy(ScrollPane.ScrollBarPolicy.ALWAYS);

        stage.setScene(new Scene(bp));

        int estimated_size = (sum * 23) + sections.size();
        if (estimated_size >= 560) {
            stage.setHeight(560);
        } else {
            System.out.println(sum);
            if (estimated_size <= 90) {
                stage.setHeight(90);
            } else {
                stage.setHeight(estimated_size);
            }
        }
        stage.setTitle("ini-reader Simulator");
        stage.getIcons().add(new Image(new File("data/favicon.png").toURI().toString()));
        stage.show();
    }

    public static void main(String[] args) {
        Application.launch(args);
    }


}
