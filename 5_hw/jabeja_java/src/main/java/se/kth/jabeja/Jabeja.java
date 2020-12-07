package se.kth.jabeja;

import static java.lang.Math.pow;
import static java.lang.Math.exp;
import org.apache.log4j.Logger;
import se.kth.jabeja.config.Config;
import se.kth.jabeja.config.NodeSelectionPolicy;
import se.kth.jabeja.io.FileIO;
import se.kth.jabeja.rand.RandNoGenerator;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class Jabeja {
  final static Logger logger = Logger.getLogger(Jabeja.class);
  private final Config config;
  private final HashMap<Integer/*id*/, Node/*neighbors*/> entireGraph;
  private final List<Integer> nodeIds;
  private int numberOfSwaps;
  private int round;
  private float T;
  private boolean resultFileCreated = false;
  private int restart;
  private int restartRounds;

  //-------------------------------------------------------------------
  public Jabeja(HashMap<Integer, Node> graph, Config config) {
    this.entireGraph = graph;
    this.nodeIds = new ArrayList(entireGraph.keySet());
    this.round = 0;
    this.numberOfSwaps = 0;
    this.config = config;
    this.T = config.getTemperature();
    this.restart = config.getRestart();
    this.restartRounds = config.getRestartRounds();
  }

  //-------------------------------------------------------------------
  public void startJabeja() throws IOException {
    for (round = 0; round < config.getRounds(); round++) {
      for (int id : entireGraph.keySet()) {
        sampleAndSwap(id);
      }

      // Ja-be-Ja SA restart -> task 2.2
      if (restart == 1 && (round % restartRounds == 0)) {
        this.T = config.getTemperature();
      }

      //one cycle for all nodes have completed.
      //reduce the temperature
      saCoolDown();
      report();

      
    }

    Config config = this.config;
      File inputFile = new File(config.getGraphFilePath());

      String outputFilePath = config.getOutputDir() +
            File.separator +
            inputFile.getName() + "_" +
            "NS" + "_" + config.getNodeSelectionPolicy() + "_" +
            "GICP" + "_" + config.getGraphInitialColorPolicy() + "_" +
            "T" + "_" + config.getTemperature() + "_" +
            "D" + "_" + config.getDelta() + "_" +
            "RNSS" + "_" + config.getRandomNeighborSampleSize() + "_" +
            "URSS" + "_" + config.getUniformRandomSampleSize() + "_" +
            "A" + "_" + config.getAlpha() + "_" +
            "SA" + "_" + config.getSaActivation() + "_" +
            "RE" + "_" + config.getRestart() + "_" +
            "RE_R" + "_" + config.getRestartRounds() + "_" +
            "R" + "_" + config.getRounds() + ".txt";

      System.out.println("outputFilePath " + outputFilePath);

  }

  /**
   * Simulated annealing cooling function
   */
  private void saCoolDown(){

    float T_min = 0.00001f;
    float delta = config.getDelta();

    // SA cooling function for the 2.1 task
    if (config.getSaActivation() == 1) {
      // forcing T to start from 1, it is mandatory with SA (there is also a command line argument)
      //this.T = 1;
      // the correct version from the articles say to set between 0.8 and 0.99
      //delta = 0.9f;
      // exponential SA cooling
      if (T > T_min) {
        T *= delta;
      }
      if (T < T_min) {
        T = T_min;
      }
    }
    // linear SA cooling (default function)
    else {
      if (T > 1)
        T -= delta;
      if (T < 1)
        T = 1;
    }
  }

  /**
   * Sample and swap algorith at node p
   * @param nodeId
   */
  private void sampleAndSwap(int nodeId) {
    Node partner = null;
    Node nodep = entireGraph.get(nodeId);

    if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
            || config.getNodeSelectionPolicy() == NodeSelectionPolicy.LOCAL) {

    // swap with random neighbors
        Integer[] randomNeighbors = getNeighbors(nodep);
    	partner = findPartner(nodeId, randomNeighbors);
    }

    if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
            || config.getNodeSelectionPolicy() == NodeSelectionPolicy.RANDOM) {

      // if local policy fails then randomly sample the entire graph
        // check that the previous if did not modified the partner reference
    	if (partner == null) {
    	    Integer[] sampleNeighbors = getSample(nodeId);
    		partner = findPartner(nodeId, sampleNeighbors);
    	}
    }
    // swap the colors
    if (partner != null) {
    	int pColorId = nodep.getColor();
    	int partnerColorId = partner.getColor();
    	nodep.setColor(partnerColorId);
    	partner.setColor(pColorId);
    	this.numberOfSwaps++;
    }
  }


  public Node findPartner(int nodeId, Integer[] nodes){

    Node nodep = entireGraph.get(nodeId);
    float alpha = config.getAlpha();

    Node bestPartner = null;
    double highestBenefit = 0;

    for(Integer node : nodes) {
    	Node nodeq = entireGraph.get(node);

    	int pColorId = nodep.getColor();
    	int qColorId = nodeq.getColor();

        int dpp = getDegree(nodep, pColorId);
        int dqq = getDegree(nodeq, qColorId);
        double oldBenefit = pow(dpp, alpha) + pow(dqq, alpha);

        int dpq = getDegree(nodep, qColorId);
        int dqp = getDegree(nodeq, pColorId);
        double newBenefit = pow(dpq, alpha) + pow(dqp, alpha);

        double ap = 0;

        // different SA mechanism task 2.1 -> acceptance probability
        if (config.getSaActivation() == 1) {
          if (config.getCustomProbability() == 1) {
            ap = exp((newBenefit - oldBenefit - 1) / this.T);
          }
          else {
            ap = exp((newBenefit - oldBenefit) / this.T);
          }
          if (ap > Math.random() && newBenefit > highestBenefit) {
            bestPartner = nodeq;
            highestBenefit = newBenefit;
          }
        }
        // standard Ja-Be-Ja case with linear decreasing
        else {
          if (newBenefit * this.T > oldBenefit && newBenefit > highestBenefit) {
            bestPartner = nodeq;
            highestBenefit = newBenefit;
          }
        }
    }
    return bestPartner;
  }

  /**
   * The the degreee on the node based on color
   * @param node
   * @param colorId
   * @return how many neighbors of the node have color == colorId
   */
  private int getDegree(Node node, int colorId){
    int degree = 0;
    for(int neighborId : node.getNeighbours()){
      Node neighbor = entireGraph.get(neighborId);
      if(neighbor.getColor() == colorId){
        degree++;
      }
    }
    return degree;
  }

  /**
   * Returns a uniformly random sample of the graph
   * @param currentNodeId
   * @return Returns a uniformly random sample of the graph
   */
  private Integer[] getSample(int currentNodeId) {
    int count = config.getUniformRandomSampleSize();
    int rndId;
    int size = entireGraph.size();
    ArrayList<Integer> rndIds = new ArrayList<Integer>();

    while (true) {
      rndId = nodeIds.get(RandNoGenerator.nextInt(size));
      if (rndId != currentNodeId && !rndIds.contains(rndId)) {
        rndIds.add(rndId);
        count--;
      }

      if (count == 0)
        break;
    }

    Integer[] ids = new Integer[rndIds.size()];
    return rndIds.toArray(ids);
  }

  /**
   * Get random neighbors. The number of random neighbors is controlled using
   * -closeByNeighbors command line argument which can be obtained from the config
   * using {@link Config#getRandomNeighborSampleSize()}
   * @param node
   * @return
   */
  private Integer[] getNeighbors(Node node) {
    ArrayList<Integer> list = node.getNeighbours();
    int count = config.getRandomNeighborSampleSize();
    int rndId;
    int index;
    int size = list.size();
    ArrayList<Integer> rndIds = new ArrayList<Integer>();

    if (size <= count)
      rndIds.addAll(list);
    else {
      while (true) {
        index = RandNoGenerator.nextInt(size);
        rndId = list.get(index);
        if (!rndIds.contains(rndId)) {
          rndIds.add(rndId);
          count--;
        }

        if (count == 0)
          break;
      }
    }

    Integer[] arr = new Integer[rndIds.size()];
    return rndIds.toArray(arr);
  }


  /**
   * Generate a report which is stored in a file in the output dir.
   *
   * @throws IOException
   */
  private void report() throws IOException {
    int grayLinks = 0;
    int migrations = 0; // number of nodes that have changed the initial color
    int size = entireGraph.size();

    for (int i : entireGraph.keySet()) {
      Node node = entireGraph.get(i);
      int nodeColor = node.getColor();
      ArrayList<Integer> nodeNeighbours = node.getNeighbours();

      if (nodeColor != node.getInitColor()) {
        migrations++;
      }

      if (nodeNeighbours != null) {
        for (int n : nodeNeighbours) {
          Node p = entireGraph.get(n);
          int pColor = p.getColor();

          if (nodeColor != pColor)
            grayLinks++;
        }
      }
    }

    int edgeCut = grayLinks / 2;

    logger.info("round: " + round +
            ", edge cut:" + edgeCut +
            ", swaps: " + numberOfSwaps +
            ", migrations: " + migrations);

    saveToFile(edgeCut, migrations);
  }

  private void saveToFile(int edgeCuts, int migrations) throws IOException {
    String delimiter = "\t\t";
    String outputFilePath;

    //output file name
    File inputFile = new File(config.getGraphFilePath());
    outputFilePath = config.getOutputDir() +
            File.separator +
            inputFile.getName() + "_" +
            "NS" + "_" + config.getNodeSelectionPolicy() + "_" +
            "GICP" + "_" + config.getGraphInitialColorPolicy() + "_" +
            "T" + "_" + config.getTemperature() + "_" +
            "D" + "_" + config.getDelta() + "_" +
            "RNSS" + "_" + config.getRandomNeighborSampleSize() + "_" +
            "URSS" + "_" + config.getUniformRandomSampleSize() + "_" +
            "A" + "_" + config.getAlpha() + "_" +
            "SA" + "_" + config.getSaActivation() + "_" +
            "RE" + "_" + config.getRestart() + "_" +
            "RE_R" + "_" + config.getRestartRounds() + "_" +
            "R" + "_" + config.getRounds() + ".txt";

    if (!resultFileCreated) {
      File outputDir = new File(config.getOutputDir());
      if (!outputDir.exists()) {
        if (!outputDir.mkdir()) {
          throw new IOException("Unable to create the output directory");
        }
      }
      // create folder and result file with header
      String header = "# Migration is number of nodes that have changed color.";
      header += "\n\nRound" + delimiter + "Edge-Cut" + delimiter + "Swaps" + delimiter + "Migrations" + delimiter + "Skipped" + "\n";
      FileIO.write(header, outputFilePath);
      resultFileCreated = true;
    }

    FileIO.append(round + delimiter + (edgeCuts) + delimiter + numberOfSwaps + delimiter + migrations + "\n", outputFilePath);
  }
}
