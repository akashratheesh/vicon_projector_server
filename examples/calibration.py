import vicon_projector_server

# New Calibration Setup
calibration = vicon_projector_server.Calibration_Setup(tracker_name="tracker@localhost",
                                                    monitor_number=0)

# Start Calibration
calibration.start()
