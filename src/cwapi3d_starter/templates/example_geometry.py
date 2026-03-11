import element_controller as ec
import cadwork
from cadwork import point_3d

def create_beams_example():
    # --- METHOD 1: Using Vectors ---
    width = 200.0
    height = 400.0
    length = 3000.0
    
    start_pt_vec = point_3d(0, 0, 0)
    
    # Define the local X axis (Direction of the beam's length)
    x_dir = point_3d(1, 0, 0) 
    
    # Define the local Z axis (Direction of the beam's height/depth)
    z_dir = point_3d(0, 0, 1)

    beam_id_vectors = ec.create_rectangular_beam_vectors(
        width, 
        height, 
        length, 
        start_pt_vec, 
        x_dir, 
        z_dir
    )
    print(f"Created beam with vectors: {beam_id_vectors}")

    # --- METHOD 2: Using Points ---
    p1 = point_3d(0, 1000, 0)     # Start point
    p2 = point_3d(3000, 1000, 0)  # End point
    
    # The 3rd point defines the beam's internal Z-axis orientation 
    # (usually "up" relative to the beam)
    p3 = point_3d(0, 1000, 100)   

    beam_id_points = ec.create_rectangular_beam_points(
        width, 
        height, 
        p1, 
        p2, 
        p3
    )
    print(f"Created beam with points: {beam_id_points}")

