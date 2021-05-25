
let data, root;
d3.json("../Task_1/data/topics.json").then((d) => {
	data = d;
	root = d3.pack(data);
	console.log(data)
	console.log(root)

	const node = svg.selectAll("g")
		.data(d3.group(root.descendants(), d => d.height))
		.join("g")
		.selectAll("g")
		.data(d => d[1])
		.join("g")
			.attr("transform", d => `translate(${d.x + 1},${d.y + 1})`);
})




const svg = d3.create("svg")
	.attr("viewBox", [0, 0, 1000, 1000])
	.style("font", "10px sans-serif")
	.attr("text-anchor", "middle")



svg.append("filter")
	.attr("id", "hi")
	.append("feDropShadow")
	.attr("flood-opacity", 0.3)
	.attr("dx", 0)
	.attr("dy", 1);

