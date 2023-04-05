# API documentation

Alles in json

## SET

{
type: "set",
data: {
[daten]
}
}

[daten]:
heizstab: boolean
motor: integer

## GET

{
type: "get",
data: {
[daten]  
 }
}

[daten]:
["motor", "heizstab", "t1", "t2"]
