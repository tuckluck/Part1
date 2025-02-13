import numpy as np
import matplotlib.pyplot as plt

def Welcome2():
    print("Welcome to the Elasto-Plastic Material Model!")

class Isotropic_Material:    #dfines a class to contain isotropic materials
    def __init__(self, stress_current, plastic_strain_current, 
                 elastic_mod, plastic_mod, yield_stress):
        #list of attributes the class will hold
        self.stress_current = stress_current
        self.plastic_strain_current = plastic_strain_current
        self.elastic_mod = elastic_mod
        self.plastic_mod = plastic_mod
        self.yield_stress = yield_stress
        
    def stress(self):
        #used to return current stress when updated
        return self.stress_current
    
    def strain(self):
        #used to return current plastic strain when updated
        return self.plastic_strain_current
    
    def mat_properties(self):
        #creates a vector of unchanging material properties for use in fucntions
        mat_prop_vec = np.empty((3))
        mat_prop_vec[0] = self.elastic_mod
        mat_prop_vec[1] = self.plastic_mod
        mat_prop_vec[2] = self.yield_stress 
        return mat_prop_vec
        
    def update_stress(self,del_strain):
        #function used to update the stress value for isotropic hardening
        current_yield_stress = self.yield_stress + self.plastic_mod * self.plastic_strain_current
        del_stress_trial = del_strain * self.elastic_mod
        stress_trial = self.stress_current + del_stress_trial
        phi_trial = abs(stress_trial) - current_yield_stress
        if phi_trial <= 0:  #meaning elastic
            self.stress_current = stress_trial
        else: #must be in plastic region
            del_plastics_strain = phi_trial / (self.elastic_mod + self.plastic_mod)
            self.stress_current = stress_trial - np.sign(stress_trial) * self.elastic_mod * del_plastics_strain
            self.plastic_strain_current = self.plastic_strain_current + del_plastics_strain
        


def create_strain_vector(vector,between_steps = 100):  
    #vector will always have an implied start of zero, but dont enter zero as the first item
    #enter the maxs and mins, alternatting between the two
    # example of running code create_strain_vector([30,-5,20,-10])
    if vector[0] == 0:   # error created if first item in the vector is zero
        raise ValueError("First entry in the vector cannot start with zero, zero is implied")
    out_vec = np.zeros(len(vector)*between_steps)  
        #initializes an ouput vector which will contain the entire input vector for
        #running the main code. This vector will include equally spaced numbers inbetween
        #the max and mins decided above
    count = 0
    for i in vector:       
        if count == 0:
            incr_vec = np.linspace(0,i,between_steps)      
            count = 1   #so the if statement will not be triggered next time through loop
            out_vec[:between_steps] = incr_vec  
            #establishes the first piece of the output vector
        else:
            #after first time through the loop this piece always active
            incr_vec = np.linspace(next_start,i,between_steps)
            #creates linearly spaced vector between each item in the input vector
            out_vec[count*between_steps:(count+1)*between_steps] = incr_vec
            #establishes where to place the incr_vec in the out_vec
            count = count+1   
        
        next_start = i  #establishes where to start next incr_vec (incremental vector)
                    
    return out_vec

def run_Iso_Hardening(mat_properties, strain_vec):
    #code used to run the Isometric Hardening simulation. Will output graph automatically
    stress = np.zeros(len(strain_vec))  #initialize stress vector to be filled
    strain = strain_vec
    for i in range(1,len(strain_vec)):
        #for every change in strain, inserts corresponding stress using above class function
        My_mat.update_stress(strain_vec[i]-strain_vec[i-1])
        stress[i] = My_mat.stress()

    # Define two vectors
    x = strain
    y = stress

    # Create the plot
    plt.plot(x, y,  linestyle='-')  #  '-' for a solid line

    # Labels and title
    plt.xlabel("Strain")
    plt.ylabel("Stress")
    plt.title("Isotropic Hardening")

    # Show the plot
    plt.show()

class Kinematic_Material:
    def __init__(self, stress_current, back_stress_current, plastic_strain_current, 
                 elastic_mod, plastic_mod, yield_stress):
        #establishes attributes the class holds
        self.stress_current = stress_current
        self.back_stress_current = back_stress_current
        self.plastic_strain_current = plastic_strain_current
        self.elastic_mod = elastic_mod
        self.plastic_mod = plastic_mod
        self.yield_stress = yield_stress
    
    def stress(self):
        #used to call current stress
        return self.stress_current
    
    def strain(self):
        #used to call current plastic strain
        return self.plastic_strain_current
                
    def back_stress(self):
        return self.back_stress_current
    
    def mat_properties(self):
        #establishes a vector with unchanging attributes
        mat_prop_vec = np.empty((3))
        mat_prop_vec[0] = self.elastic_mod
        mat_prop_vec[1] = self.plastic_mod
        mat_prop_vec[2] = self.yield_stress 
        return mat_prop_vec
        
    def update_stress(self,del_strain):
        #used to update stress for the incremental kinematic hardening scenerio       
        stress_trial = self.stress_current + self.elastic_mod * del_strain
                
        back_trial = self.back_stress_current
        nu_trial = stress_trial - back_trial
        phi_trial = abs(nu_trial)-self.yield_stress
        if phi_trial <= 0:  #meaning elastic
            self.stress_current = stress_trial
        else: #must be in plastic region
            del_plastics_strain = phi_trial / (self.elastic_mod + self.plastic_mod)
            self.stress_current = stress_trial - np.sign(nu_trial) * self.elastic_mod * del_plastics_strain
            self.back_stress_current = back_trial +np.sign(nu_trial) * self.plastic_mod * del_plastics_strain
            self.plastic_strain_current = self.plastic_strain_current + del_plastics_strain
        

def run_Kinematic_Hardening(mat_properties, strain_vec):
    #code to run the Kinematic Hardening scenerio, will run a plot automatically
    stress = np.zeros(len(strain_vec))
    strain = strain_vec
    for i in range(1,len(strain_vec)):
        My_mat.update_stress(strain_vec[i]-strain_vec[i-1])
        stress[i] = My_mat.stress()

    # Define two vectors
    x = strain
    y = stress

    # Create the plot
    plt.plot(x, y,  linestyle='-')  # 'o' for markers, '-' for a solid line

    # Labels and title
    plt.xlabel("Strain")
    plt.ylabel("Stress")
    plt.title("Kinematic Hardening")

    # Show the plot
    plt.show()

        
        
        
        
        
      
        
        
        
        
        
    

