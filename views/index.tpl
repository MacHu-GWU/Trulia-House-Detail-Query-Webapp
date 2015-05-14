<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Trulia Crawler App</title>
</head>
<body>


<form action="/result" method="POST" enctype="multipart/form-data">
  Select a csv File: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
</form>

%if batch_query_result:
	<a href={{batch_query_result}}>download json</a>
%else:
	<a href=example_input.txt>click here to view sample tab seperated csv file</a>
%end
</body>
</html>