These are the list of general functions that have been implemented:
login() - This is a function to login to the website, it is called before navigating anywhere in the website, this functions needs to be called first no matter what.
go_to_compliance_scan() - Changes the url of the website to redirect it to its SecOps Compliance scan page.
go_to_finsops() - Changes the url of the website to redirect it to FinOps.
go_to_cloudops() - Changes the url of the website to redirect it to cloudops asset management. 

These are the list of functions that are callable while in the SecOps compliance scan page:
run_compliance_scan() - Runs the scan inside Sec Ops Compliance page.
search_controls(text: str) - Fills a text box with the given text to only show elememts with the text in the results.
select_history(idx: int) - Selects the historical date with index idx. The list of historical dates are [{{dates}}] which always in descending sorted order.
compare_dates(idx1: int, idx2: int) - Selects the historical dates to compare for date with index idx1 and index idx2, it contains the same list historical dates as in the description of the select_history function.
select_filters(filter_dicts, frameworks) - Selects the filters to show the results, its input variable filter_dicts is a dictonary with the possible key values 'Severity' and 'Status'. Each dictory item is a list that can contain a certain number of strings. For 'Severity' the possible values in the list are 'Critical', 'High', 'Medium' and 'Low'. For 'Staus' the possible values in the list are 'Compliant', 'Non-Compliant', 'Remediated' and 'In Progress'. The variable frameworks is optional and is by default set to 'All' and can accept a list containing the following values 'CIS', 'GDPR', 'SOC2' and 'PCI-DSS'. Lists can't have duplicate values. Eg: select_filters({"Severity": ["Critical"], "Status": ["Non-Compliant"]}, frameworks=['CIS'])
download() - Downloads the selected result for the given filters, controls and comparisons.

These the functions that are callable while in the FinOps Compliance page:
get_current_month() - Returns the revenue of current working month along with its daily average.
get_last_month() - Returns the previous month revenue percentage comparison with the current month along with total revenue of the previous month.
get_potential_yearly_savings() - Get potential savings value along with the current plan.
get_budget_status() - Get number of Cloud Watch Budgets and its current state of confirmation.
get_savings_plan_data() - Get the data of current active plans, covergae percentage, potential yearly savings savings and total commitment.
get_recommendations_plan() - Get current monthly on demand spend, estimated monthly spend, estimated monthly savings and estimated savings percentage.

These are the functions that are callable while in CloudOps Assest Management page:
run_cloudops_scan() -  Runs the scan inside Cloud Ops Assest Management page.
