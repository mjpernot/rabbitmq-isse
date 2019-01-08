# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [0.3.6] - 2018-11-26
### Changed
- daemon_rmq_2_isse.main:  Replaced backslash (/) with parenthesis "()" for easier use of print.
- run_program:  Moved program lock to outside of "for" loop.
- non_proc_msg:  Removed "create_body" call as it is done internally in the class.

### Fixed
- non_proc_msg:  Changed "*kwargs" to "**kwargs".


## [0.3.5] - 2018-05-21
### Changed
- Documentation updates.


## [0.3.4] - 2018-05-11
### Changed
- daemon_rmq_2_isse.main:  Added "-d" option to the argument list and required list.


## [0.3.3] - 2018-05-10
### Changed
- Changed lclass to rabbit_lib to standardize directory naming.
- non_proc_msg:  Added information to subject line in emails to be clearer.
- find_files:  Removed redundant os.path.join commands.
- find_files:  Added additional information to log entry if nothing found.
- run_program:  Added additional log entries to log during initialization.


## [0.3.2] - 2018-05-09
### Added
- is_valid_name:  Determine if the file name meets the search criteria.

### Changed
- process_msg:  Added call to see if file name meets file criteria.


## [0.3.1] - 2018-05-08
### Changed
- rmq_2_isse:  Changed "gen_libs" calls to new naming schema.
- rmq_2_isse:  Changed "arg_parser" calls to new naming schema.
- daemon_rmq_2_isse:  Changed "arg_parser" calls to new naming schema.


## [0.3.0] - 2018-05-04
- Field release.


## [0.2.0] - 2018-02-26
- Beta version release


## [0.1.15] - 2018-02-26
### Changed
- Documentation updates.


## [0.1.14] - 2018-02-22
### Changed
- rmq_2_isse:  Moved rabbitmq_class to sub-directory lclass.


## [0.1.13] - 2018-02-21
### Changed
- daemon_rmq_2_isse.main:  Added a flavor id to the daemon pidfile name to allow multiple instances.
- validate_create_settings:  Changed cfg.log_file value to be unique for multiple instances.


## [0.1.12] - 2018-02-20
### Changed
- Documentation updates.


## [0.1.11] - 2018-02-19
### Changed
- Documentation updates.


## [0.1.10] - 2018-02-16
### Fixed
- find_files:  Add correct year/month to file name path if found in previous year/month directory.
- process_msg:  Corrected logic error when detecting max resends on messages.


## [0.1.9] - 2018-02-15
### Fixed
- find_files:  Added leading zeros to month variable to pad it out to two digits.


## [0.1.8] - 2018-02-14
### Added
- daemon_rmq_2_isse.py:  Runs the rmq_2_isse program as a daemon/service.


## [0.1.7] - 2018-02-13
### Changed
- main:  Added ability for program to accept arguments from command line or another program.


## [0.1.6] - 2018-02-12
### Changed
- validate_create_settings:  Replaced gen_libs.Chk_Crt_Dir with gen_libs.chk_crt_dir.
- validate_create_settings:  Replaced gen_libs.Chk_Crt_File with gen_libs.chk_crt_file.


## [0.1.5] - 2018-02-08
### Changed
- is_valid_msg:  Changed logging to be more descriptive.
- non_proc_msg:  Changed logging to be more descriptive.
- find_files:  Changed logging to be more descriptive.
- is_valid_ext:  Changed logging to be more descriptive.
- process_msg:  Changed logging to be more descriptive.
- monitor_queue:  Changed logging to be more descriptive.


## [0.1.4] - 2018-02-07
### Changed
- Documentation updates.


## [0.1.3] - 2018-02-06
### Changed
- Documentation updates.


## [0.1.2] - 2018-02-05
### Fixed
- process_msg:  Incorrect order of logging messages.

### Changed
- validate_create_settings:  Changed proc_file name to include day of the month in file name.


## [0.1.1] - 2018-02-02
### Fixed
- find_files:  Add directory path to each file name in the file_list list array.
- process_msg:  Added missing cfg argument to non_proc_msg function calls.
- non_proc_msg:  Replaced RQ.exchange_name with RQ.exchange and added names arguments to write_file call.

### Changed
- process_msg:  Moved the writing to process file to earlier in the loop.


## [0.1.0] - 2018-01-29
- Initial Alpha release.


## [0.0.19] - 2018-01-26
### Changed
- non_proc_msg:  Changed gen_libs.Write_File2 to gen_libs.write_file and system.Mail to gen_class.Mail.
- process_msg:  Changed gen_libs.Write_File2 to gen_libs.write_file.
- run_program:  Changed gen_class.Program_Lock to gen_class.ProgramLock along with new exception.


## [0.0.18] - 2018-01-26
### Changed
- Documentation updates.


## [0.0.17] - 2018-01-23
### Changed
- Documentation updates.


## [0.0.16] - 2018-01-19
### Changed
- Documentation updates.


## [0.0.15] - 2018-01-18
### Changed
- Documentation updates.


## [0.0.14] - 2018-01-11
### Changed
- Documentation updates.


## [0.0.13] - 2018-01-10
### Changed
- run_program:  Refactor logic test on the status flag.


## [0.0.12] - 2018-01-09
### Fixed
- process_msg:  Parsing the body of the message to be read by the loop.


## [0.0.11] - 2018-01-08
### Changed
- Documentation updates.


## [0.0.10] - 2018-01-05
### Fixed
- find_files:  Corrected error in reference to os.path.join lines.


## [0.0.9] - 2018-01-04
### Fixed
- non_proc_msg:  Corrected incorrect module call to gen_libs.Get_Time.


## [0.0.8] - 2018-01-03
### Changed
- Documentation updates.


## [0.0.7] - 2018-01-02
### Fixed
- validate_create_settings:  Incorrect proc_name path setting.


## [0.0.6] - 2017-12-28
### Changed
- non_proc_msg: Added .txt extension to file name.


## [0.0.5] - 2017-12-22
### Changed
- validate_create_settings:  Call to gen_libs.get_base_dir to get base directory path.
- process_msg:  Replaced file_search_cnt with gen_libs.file_search_cnt.
- find_files:  Replaced month_delta with gen_libs.month_delta.

### Removed
- file_search_cnt function.
- month_delta function.


## [0.0.4] - 2017-12-19
### Added
- month_delta:  Produces a month delta based on date passed to it.
- find_files: Find one or more files from in a directory.
- is_valid_ext: Validate the file extension of the file to be copied.

### Changed
- validate_create_settings: Added additional checks on other configuration settings.


## [0.0.3] - 2017-12-18
### Added
- file_cnt:  Search and count line instances in a file.
- validate_create_settings: Validate configuration and creation of settings.
- is_valid_msg: Checks to see that the message is valid format.
- non_proc_msg:  Process non-processed messages.

### Changed
- run_program:  Replaced load_cfg with gen_libs.Load_Module and validate_create_settings call.
- process_msg:  Refactored the logic in the function.

### Removed
- load_cfg function.


## [0.0.2] - 2017-12-15
### Changed
- rmq_2_isse:  Rename process_message function to monitor_queue.

### Added
- callback: Initiate the message processing.
- process_msg:  Process message from RabbitMW queue.

### Fixed
- load_cfg: Corrected error in configuration check.


## [0.0.1] - 2017-12-14
### Added
- main: Initate program.
- run_program: Control flow of program.
- process_message: Process message in a RabbitMQ queue.
- load_cfg: Load configuration file and validate.
- help_message: Programs help message and version.

