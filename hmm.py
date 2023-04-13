import numpy as np
import itertools

from numpy.core.fromnumeric import prod


class HMM_model():

    def __init__(self):
        self.states = ["morning", "noon", "evening"]
        self.emissions = ["tired", "awake"]
        self.observations = []
        self.transition_propability_threshold = 0.05
        self.t_matrix = [ np.random.dirichlet(np.full(3, 1)).tolist(),
                         np.random.dirichlet(np.full(3, 1)).tolist(),
                         np.random.dirichlet(np.full(3, 1)).tolist() ]
        self.e_matrix = [ np.random.dirichlet(np.full(2, 1)).tolist(),
                         np.random.dirichlet(np.full(2, 1)).tolist(),
                         np.random.dirichlet(np.full(2, 1)).tolist() ]
        self.get_path = True
        #print("TMatrix: ")
        #for i in self.t_matrix:
            #print(i)
        #print("EMatrix: ")
        #for i in self.e_matrix:
            #print(i)
        self.hmmPath()

    def hmmPath(self):
        print("")
        print("Enter a sequence of observations seperated by spaces from the list: " + str(self.emissions))
        print("Type exit to end the program")
        while(self.get_path):
            self.observations = input("Observation: ").rsplit()
            if self.observations[0] == "exit":
                break
            #print(self.observations)
            #print(self.validEmission(self.observations, self.emissions))
            if (self.validEmission(self.observations, self.emissions)):
                translation_set = []
                for i in range(len(self.observations)):
                    x = self.observations[i]
                    translation_set.append(self.emissionSet(x))
                #print("Translation Set: ")
                #print([("            " + x) for x in self.states])
                for i in range(len(translation_set)):
                    print(self.observations[i] + ": " + str(translation_set[i]))
                S3 = self.cartesianProduct(translation_set)
                possiable_paths = self.validTransitions(S3)
                print("Available paths: " + str(len(S3)))
                #print([[round(y,5) for y in x] for x in S3])
                print("")
                print("Possiable paths: " + str(len(possiable_paths)))
                #print([[round(y,5) for y in x] for x in possiable_paths])
                self.output = self.pathProbability(possiable_paths, self.observations)
                print("")
                print("Individual Path Probability: " + str(self.output[0]))
                print("")
                print("Overall Path Probability: " + str(self.output[1]))
                print("")
                print("Transition Strings: " + str(self.output[2]))
                #self.get_path = False



    def cartesianProduct(self, matrix):
        tmp = []
        for i in itertools.product(*matrix):
            tmp.append(i)
        return tmp
                

    def validEmission(self, e_input, e_set):
        for i in e_input:
            if ((i in e_set) == False):
                return False
        return True
    
    def validTransitions(self, t_seq):
        possiable_transitions = []
        for i in range(len(t_seq)):
            path_possible = True
            for j in range(len(t_seq[i])):
                if (j + 1 == len(t_seq[i]) or not path_possible):
                    break
                if t_seq[i][j] <= self.transition_propability_threshold:
                    path_possible = False
            if path_possible:
                possiable_transitions.append(t_seq[i])
        return possiable_transitions

    def emissionSet(self, emission):
        j = self.emissions.index(emission)
        e_set = []
        for i in range(len(self.states)):
            e_set.append(self.e_matrix[i][j])
        return e_set

    def pathProbability(self, possiable_paths, observed):

        a = np.array([1, 2, 3])
        

        highest_probability = 0
        highest_probable_path = 0
        transposed_e_matrix = np.array(self.e_matrix).T
        transposed_e_matrix = [[round(y, 5) for y in x] for x in transposed_e_matrix]
        transition_strings = []
        for i in range(len(possiable_paths)):
            probability = prod(possiable_paths[i])
            for j in range(len(possiable_paths[i])):
                if j + 1 == len(possiable_paths[i]):
                    break
                probability = probability * transposed_e_matrix[self.emissions.index(observed[j])][self.emissions.index(observed[j + 1])]
            if (probability > highest_probability):
                highest_probability = probability
                highest_probable_path = possiable_paths[i]
                transition_strings = []
                for k in range(len(highest_probable_path)):
                    transition_strings.append(self.states[(transposed_e_matrix[self.emissions.index(observed[k])]).index(round(highest_probable_path[k], 5))])
        return (highest_probable_path, highest_probability, transition_strings)

            
                

def main():
    x = HMM_model()
    x.hmmPath()


main()
