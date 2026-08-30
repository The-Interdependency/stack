# ratios: loc_comments=33:13 imports_exports=2:2 calls_definitions=15:2
"""
tests/proof_check.py
Empirical verification of PCNA Spectral Graph properties.
Compares 7:1 Ring vs 7:3 Heptagram.
"""

import numpy as np
import scipy.linalg as la

def get_circulant_matrix(n, offsets):
    """Generates the Adjacency Matrix for a circulant graph."""
    matrix = np.zeros((n, n))
    for i in range(n):
        for k in offsets:
            neighbor = (i + k) % n
            matrix[i][neighbor] = 1
            matrix[neighbor][i] = 1
    return matrix

def analyze_topology(name, offsets):
    n = 7
    adj = get_circulant_matrix(n, offsets)
    
    # Calculate Eigenvalues
    evals = la.eigvals(adj).real
    evals = np.sort(evals)[::-1] # Sort descending
    
    # Spectral Gap (lambda_0 - lambda_1)
    # Note: lambda_0 is regular degree (2)
    gap = evals[0] - evals[1]
    
    print(f"\n--- {name} (Offsets {offsets}) ---")
    print(f"Eigenvalues: {np.round(evals, 3)}")
    print(f"Spectral Gap: {gap:.3f} (Larger is faster mixing)")
    
    # Diameter check (hops to cross graph)
    # Simple BFS for node 0
    hops = [-1] * n
    hops[0] = 0
    queue = [0]
    while queue:
        current = queue.pop(0)
        for idx, connected in enumerate(adj[current]):
            if connected == 1 and hops[idx] == -1:
                hops[idx] = hops[current] + 1
                queue.append(idx)
    
    print(f"Diameter: {max(hops)}")

if __name__ == "__main__":
    print("PCNA Topology Mathematical Verification")
    
    # Standard Ring (Nearest Neighbor)
    analyze_topology("Standard Ring", [1])
    
    # PCNA Heptagram (The 7:3 star)
    analyze_topology("PCNA Heptagram", [3])
# ratios: loc_comments=33:13 imports_exports=2:2 calls_definitions=15:2
