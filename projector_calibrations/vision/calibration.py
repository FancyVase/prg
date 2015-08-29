import bad_demo
import initial_calibration
import projector_camera_calibration
import calculate_homographies
import grid_demo

def main():
	# show the projectors before being calibrated
	bad_demo.main()

	# calibrate one projector manually
	master_to_world = initial_calibration.main()

	# find projector and camera point pairs for all three projectors
	matches = projector_camera_calibration.main()

	# find projector to world homographies
	homographies = calculate_homographies.main()
	
	# demo accuracy of homographies
	grid_demo.main(homographies)

if __name__ == '__main__':
	main()