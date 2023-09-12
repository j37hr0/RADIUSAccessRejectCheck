# RADIUSAccessRejectCheck

This is a simple python script to run a query and check if the RADIUS is recieving access-rejects  
This shouldn't really happen, so we need to check and alert for this, as there was an edge case  
where a machine was excessively failing (it didn't exist in the auth table)
