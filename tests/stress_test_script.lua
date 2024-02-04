-- a stress test script for the API using wrk2
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
-- wrk.headers["Authorization"] = "Bearer YOUR_ACCESS_TOKEN"  -- Add your authentication token if required

-- Example payload for the API
wrk.body = '{"id":"65876e949d7c56efe8d35f8a","nodes":[{"id":"add0dcc9-299b-4e40-9c7a-c4cd10a79a3a","type":"inputDataNode","position":{"x":65,"y":372},"positionAbsolute":{"x":0,"y":0},"data":{"file":"/mnt/Storage/Projects/PrediKit/examples/sample_data/airline_bumping.csv"},"width":64,"height":81,"selected":true,"dragging":false},{"id":"de384a96-e911-4587-b490-a85703e3bf97","type":"basicFilterNode","position":{"x":379,"y":408},"positionAbsolute":{"x":379,"y":408},"data":{"column":"year","value":"2016","caseSensitive":true,"operator":"greater"},"width":64,"height":81},{"id":"026c392f-ece8-424e-b94a-b1ed9c44e50b","type":"outputDataNode","position":{"x":690,"y":392},"positionAbsolute":{"x":690,"y":392},"data":{"format":"csv","filename":"some_shit","indexColumn":false},"width":64,"height":98,"selected":false,"dragging":false}],"paths":[["add0dcc9-299b-4e40-9c7a-c4cd10a79a3a","de384a96-e911-4587-b490-a85703e3bf97","026c392f-ece8-424e-b94a-b1ed9c44e50b"]]}'  -- Modify as per your API payload

