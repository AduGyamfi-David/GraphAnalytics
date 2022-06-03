var svg = d3.select("svg")
const width = svg.attr("width");
const height = svg.attr("height");

var links, nodes;
var xml_http_req = new XMLHttpRequest();

getGraph()

function getGraph() {
	xml_http_req.open("GET", "/get-graph", true);
	xml_http_req.setRequestHeader("Content-type", "application/json; charset=utf-8");
	xml_http_req.onreadystatechange = function () {
		if (xml_http_req.readyState == 4 && xml_http_req.status == 200) {
			let data = JSON.parse(xml_http_req.responseText);
			links = data.links;
			nodes = data.nodes;

			const simulation = d3
				.forceSimulation(nodes)
				.force(
					"link", 
					d3.forceLink(links)
						.id(d => d.id)
				)
				.force(
					"charge", 
					d3.forceManyBody()
				)
				.force(
					"center", 
					d3.forceCenter(width / 2, height / 2)
				);
			
			const link = svg
				.append("g")
				.attr("stroke", "#999")
				.attr("stroke-opacity", 0.6)
				.selectAll("line")
				.data(links)
				.join("line")
				.attr("stroke-width", 1);

			const node = svg
				.append("g")
				.attr("stroke", "#fff")
				.attr("stroke-width", 1.5)
				.selectAll("circle")
				.data(nodes)
				.join("circle")
				.attr("r", 5)
				.attr(
					"fill",
					(d) => {
						return d.fraud ? "red" : "orange";
					}
				)
				.call(drag(simulation));

			simulation.on("tick", () => {
				link
					.attr("x1", (d) => d.source.x)
					.attr("y1", (d) => d.source.y)
					.attr("x2", (d) => d.target.x)
					.attr("y2", (d) => d.target.y);
				
				node
					.attr("cx", (d) => d.x)
					.attr("cy", (d) => d.y);
			});
		}
	};

	xml_http_req.send();
}

let drag = (simulation) => {
	function DragStarted(event) {
		if (!event.active) simulation.alphaTarget(0.3).restart();
		event.subject.fx = event.subject.x;
		event.subject.fy = event.subject.y;
	}

	function Dragged(event) {
		event.subject.fx = event.x;
		event.subject.fy = event.y;
	}

	function DragEnded(event) {
		if (!event.active) simulation.alphaTarget(0);
		event.subject.fx = null;
		event.subject.fy = null;
	}

	return d3.drag()
		.on("start", DragStarted)
		.on("drag", Dragged)
		.on("end", DragEnded)
}