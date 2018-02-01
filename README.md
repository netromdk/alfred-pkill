# alfred-pkill
Kill processes via Alfred app workflow.

Use keyword `kill` to initiate the workflow. The input is used to fuzzy-filter against all running processes. If any result is actioned it will be killed with `kill -TERM PID`.
