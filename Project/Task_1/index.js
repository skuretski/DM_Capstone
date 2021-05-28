const height = 600;
const width = 1000;
const diameter = Math.min(width*0.9, height*0.9);

let data;

d3.json("../Task_1/data/topics.json").then((d) => {
	data = d;
	console.log(data.children)
	let layout = d3.pack().size([width, height])
	let root = d3.hierarchy(data)
	layout(root)
	console.log(root.descendants())

	const svg = d3.select("#viz").append("svg")
		.attr("width", width)
		.attr("height", height)
		.style("display", "block")
		.style("margin", "auto")
		.style("font", "10px sans-serif")
		.attr("text-anchor", "middle")
	
	const node = svg.append("g")
		.selectAll("circle")
		.data(root.descendants())
		.join("g")
		.selectAll("g")
		.data(root.descendants())
		.join("g")

	node.append("circle")
		.attr("r", d => d.r)
		.attr("fill", d => color(d.height))

  // const leaf = node.filter(d => !d.children);
  
  // leaf.select("circle")
  //     .attr("id", d => (d.leafUid = DOM.uid("leaf")).id);

  // leaf.append("clipPath")
  //     .attr("id", d => (d.clipUid = DOM.uid("clip")).id)
  //   .append("use")
  //     .attr("xlink:href", d => d.leafUid.href);

  // leaf.append("text")
  //     .attr("clip-path", d => d.clipUid)
  //   .selectAll("tspan")
  //   .data(d => d.data.name.split(/(?=[A-Z][a-z])|\s+/g))
  //   .join("tspan")
  //     .attr("x", 0)
  //     .attr("y", (d, i, nodes) => `${i - nodes.length / 2 + 0.8}em`)
  //     .text(d => d);

  // node.append("title")
  //     .text(d => `${d.ancestors().map(d => d.data.name).reverse().join("/")}\n${format(d.value)}`);
    
  // svg.node()
})





