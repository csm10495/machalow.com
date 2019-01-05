<?php 

$command = escapeshellcmd('./hfqpdb_rss_cleanup.py');
$output = shell_exec($command);
echo $output;

?>