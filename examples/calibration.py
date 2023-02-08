import vicon_projector_server



calibration = vicon_projector_server.Calibration_Setup(tracker_name="tracker@localhost", monitor_number=1)

calibration.start()
