from main import jmeter_log_files, update_csv, remove_elements
#remove elements from JSON
remove_elements("outParams", "appdate")

#update time in CSV
update_csv(12, 16)

#jmeter print log files based on status
jmeter_log_files("resources/Jmeter_log1.jtl")