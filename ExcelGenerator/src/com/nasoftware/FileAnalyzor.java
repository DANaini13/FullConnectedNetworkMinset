package com.nasoftware;

/**
 * Created by zeyongshan on 1/29/18.
 */

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

class FileAnalyzer {
    private String fileName;
    private Integer trainResult[][] = new Integer[10][10];
    private Integer testResult[][] = new Integer[10][10];
    private Float trainProcess[];
    private Float testProcess[];
    public Double trainAccuracy;
    public Double testAccuracy;
    public Integer trainTotal;
    public Integer testTotal;

    public String toString() {
        String result = "";
        result += "Training Set:\n";
        for (int x = 0; x < 10; ++x) {
            for (int y = 0; y < 10; ++y) {
                result += trainResult[x][y];
                result += "\t";
            }
            result += "\n";
        }
        result += "Total: " + trainTotal;
        result += "\nAccuracy: " + trainAccuracy;

        result += "\n\n\nTesting Set:\n";
        for (int x = 0; x < 10; ++x) {
            for (int y = 0; y < 10; ++y) {
                result += testResult[x][y];
                result += "\t";
            }
            result += "\n";
        }
        result += "Total: " + testTotal;
        result += "\nAccuracy: " + testAccuracy;

        result += "\nTrain History:\n";
        for (float x:trainProcess) {
            result += x + "\n";
        }
        result += "\nTest History:\n";
        for (float x:testProcess) {
            result += x + "\n";
        }
        return result;
    }

    public FileAnalyzer(String fileName) {
        this.fileName = fileName;
        for (int x = 0; x < 10; ++x) {
            for (int y = 0; y < 10; ++y) {
                trainResult[x][y] = 0;
                testResult[x][y] = 0;
            }
        }
        analyze();
    }
    private void analyze() {
        File file = new File(fileName);
        try {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String temp = null;
            int i = 0;
            int j = 0;
            Float[] trainProcess = new Float[20000];
            Float[] testProcess = new Float[20000];
            while ((temp = reader.readLine()) != null) {
                String[] parts = temp.split("-");
                if(Integer.parseInt(parts[0]) == 1) {
                    trainProcess[i] = Float.parseFloat(parts[1]);
                    trainProcess[i] = trainProcess[i] * 100;
                    trainProcess[i+1] = new Float(-1.0);
                    ++i;
                }
                if(Integer.parseInt(parts[0]) == 2) {
                    testProcess[j] = Float.parseFloat(parts[1]);
                    testProcess[j] = testProcess[j] * 100;
                    trainProcess[i+1] = new Float(-1.0);
                    testProcess[j+1] = new Float(-1.0);
                    ++j;
                }
                if(Integer.parseInt(parts[0]) == 3) {
                    testResult[Integer.parseInt(parts[1])][Integer.parseInt(parts[2])] += 1;
                }
            }
            this.trainProcess = new Float[i];
            this.testProcess = new Float[j];
            for(int x = 0; x < i; ++x) {
                if(trainProcess[x] == -1)
                    break;
                this.trainProcess[x] = trainProcess[x];
            }
            for(int x = 0; x < j; ++x) {
                if(testProcess[x] == -1)
                    break;
                this.testProcess[x] = testProcess[x];
            }
            if (reader != null) {
                try {
                    reader.close();
                    Integer sum = 0;
                    double correct = 0;
                    for (int x = 0; x < 10; ++x) {
                        for (int y = 0; y < 10; ++y) {
                            sum += trainResult[x][y];
                            if (x == y) {
                                correct += trainResult[x][y];
                            }
                        }
                    }
                    this.trainTotal = sum;
                    this.trainAccuracy = correct / sum;
                    sum = 0;
                    correct = 0;
                    for (int x = 0; x < 10; ++x) {
                        for (int y = 0; y < 10; ++y) {
                            sum += testResult[x][y];
                            if (x == y) {
                                correct += testResult[x][y];
                            }
                        }
                    }
                    this.testTotal = sum;
                    this.testAccuracy = correct / sum;
                } catch (IOException e) {

                }
            }
        } catch (IOException e) {
            System.err.print("cannot find file!");
            System.exit(-1);
        }
    }
}
