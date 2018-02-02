# alfred-pkill
Kill processes via Alfred app workflow.

Use keyword `kill` to initiate the workflow. The input is used to fuzzy-filter against all running processes. If any result is actioned it will be killed with `kill -TERM PID`. By using modifiers, the `kill` command will use `-KILL` with ⌘↵, `-STOP` with ⌃↵, and `-TERM` with ↵ normally.

The `killall` keyword can be used in the same way but will kill all filtered process results.

The workflow automatically checks for new releases. With a 7 day frequency, it will check and if an update is available, then it shows an item at the top in Alfred that will update the workflow when actioned/auto-completed.
