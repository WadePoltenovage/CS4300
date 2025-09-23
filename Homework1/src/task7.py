import numpy as np

def calculate_array_stats(size=100, seed=42):
    # Set the random seed
    np.random.seed(seed)
    
    # Generate a random array of floating-point numbers
    data_array = np.random.rand(size)
    
    # Calculate the mean and standard deviation 
    mean_value = np.mean(data_array)
    std_dev_value = np.std(data_array)
    
    return (mean_value, std_dev_value)

if __name__ == "__main__":
    print("Calculating statistics for a random NumPy array...")
    mean, std_dev = calculate_array_stats()
    
    print(f"Mean: {mean:.4f}")
    print(f"Standard Deviation: {std_dev:.4f}")

