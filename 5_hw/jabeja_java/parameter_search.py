import subprocess 
import numpy as np
import pandas as pd


def parse_output(stdout):
    str_stdout = str(stdout)
    lines = str_stdout.split(sep="\\n")

    result = lines[-3]
    out_file = lines[-2]
    graph_info = lines[:2]

    split_1 = result.split(sep="-")
    #print(lines)
    #print(split_1)
    raw_results = split_1[3].split(sep=",")
    #print(raw_results)

    results = {}
    results["round"] = 0
    results["edgeCut"] = 0
    results["swaps"] = 0
    results["migrations"] = 0
    
    values = []
    for result_str in raw_results:
        split = result_str.split(sep=':')
        value = split[1].replace(' ', '')
        values.append(value)
    
    results["round"] = values[0]
    results["edgeCut"] = values[1]
    results["swaps"] = values[2]
    results["migrations"] = values[3]

    out_split = out_file.split(' ')
    out_file = out_split[1]

    return results, graph_info, out_file


def run_jabeja(parameters):
    print("----------------------------------------------------")
    print(parameters)

    # Run command to start JaBeJa computation    
    command = [
        "./run.sh",
        "-alpha", str(parameters['alpha']),
        "-delta", str(parameters['delta']),
        "-graph", str(parameters['graph']),
        "-graphInitColorSelectionPolicy", str(parameters['graphInitColorSelectionPolicy']),
        "-nodeSelectionPolicy", str(parameters['nodeSelectionPolicy']),
        "-numPartitions", str(parameters['numPartitions']),
        "-outputDir", str(parameters['outputDir']),
        "-randNeighborsSampleSize", str(parameters['randNeighborsSampleSize']),
        "-restart", str(parameters['restart']),
        "-restartRounds", str(parameters['restartRounds']),
        "-rounds", str(parameters['rounds']),
        "-saActivation", str(parameters['saActivation']),
        "-seed", str(parameters['seed']),
        "-temp", str(parameters['temp']),
        "-uniformRandSampleSize", str(parameters['uniformRandSampleSize']),
        "-custom", str(parameters['customProbability'])
    ]
    
    out = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()

    # Here I have to parse the stdout string to interpret the value of edge cut.
    results, graph_info, out_file = parse_output(stdout)

    results["GraphInfo"] = graph_info
    results["OutFile"] = out_file
    
    return results
    


if __name__ == '__main__':

    graphs = ['./graphs/3elt.graph', './graphs/add20.graph', './graphs/twitter.graph']    
    t_values = np.array([2])
    selection_policy = np.array(['ROUND_ROBIN', 'BATCH']) # , 'ROUND_ROBIN', 'RANDOM'])
    delta_values = np.array([0.003])

    init_policies = ['ROUND_ROBIN', 'BATCH']
    
    for policy in init_policies:

        for graph in graphs:

            results = []

            for delta in delta_values:

                # Command line arguments and values for running Ja-Be-Ja
                params = {
                    'alpha': 2.0,
                    'delta': delta,
                    'graph': graph,
                    'graphInitColorSelectionPolicy': policy, # Either: RANDOM, ROUND_ROBIN, BATCH
                    'nodeSelectionPolicy': 'HYBRID', # Either: RANDOM, LOCAL, HYBRID
                    'numPartitions': 4,
                    'outputDir': './output',
                    'randNeighborsSampleSize': 3, # As default value
                    'restart': 0, # Restart activation, default 0
                    'restartRounds': 400, # Number of rounds for restart
                    'rounds': 1000,
                    'saActivation': 0, # Activates the simulated annealing
                    'seed': 0,
                    'temp': np.random.choice(t_values, 1)[0], # Simulated annealing temperature
                    'uniformRandSampleSize': 6,
                    'customProbability': 0
                }

                result = run_jabeja(parameters=params)
                result["delta"] = delta
                results.append(result) 

                print(result)      
                
            df = pd.DataFrame(results)
            graph_name = graph.replace("./graphs/", "")
            df.to_csv(path_or_buf='./plot/tuning/Task1-NoAnnealing/better_TASK1_' + policy + '_' + graph_name + '.csv')

        # By correctly parsing the results string we can retreive the results with this paramenter run
        # Now the fun part comes: looping and choosing paramenters in onrder to find the best edge cut

