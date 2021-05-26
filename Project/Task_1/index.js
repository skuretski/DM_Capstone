const height = 600;
const width = 1000;
const diameter = Math.min(width*0.9, height*0.9);

let data;

d3.json("../Task_1/data/topics.json").then((d) => {
	data = d;
	console.log(data)
	let layout = d3.pack().size([width, height])
	let root = d3.hierarchy(data)
	console.log(root)
	
	const svg = d3.select("#viz").append("svg")
		.attr("width", width)
		.attr("height", height)
		.style("display", "block")
		.style("margin", "auto")
	
	const node = svg.append("g")
		.selectAll("circle")
		.data(root.descendants().slice(1))
		.join("circle")
			.attr("fill", d => d.words ? ConvolverNode(d.value) : "white")
})





