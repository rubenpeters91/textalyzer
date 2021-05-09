"use strict";

function d3_bar(data) {
    data = data.sort((a, b) => d3.descending(a.freq, b.freq))

    // Set variables
    const margin = { left: 60, right: 10, top: 30, bottom: 10 };
    let height = 350
    const width = 400;

    // Build svg
    let graph = d3.select("#plotcontainer")
        .append("svg")
        .attr("viewBox", [0, 0, width, height])
        .style("fill", "steelblue");

    // Scales
    let x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.freq)])
        .range([margin.left, width - margin.right]);

    let y = d3.scaleBand()
        .domain(d3.range(data.length))
        .rangeRound([margin.top, height - margin.bottom])
        .padding(0.1);

    // Bars
    let bar = graph.selectAll("rect")
        .data(data)
        .join("rect")
        .attr("x", x(0))
        .attr("y", (d, i) => y(i))
        .attr("width", 0)
        .attr("height", y.bandwidth())
        .on("mousemove", mouseMove)
        .on("mouseover", mouseEnter)
        .on("mouseout", mouseLeave)

    // Axis
    let xAxis = d3.axisTop(x)
    let yAxis = d3.axisLeft(y)
        .tickFormat(i => data[i].term)
        .tickSizeOuter(0);

    graph.append("g")
        .attr("transform", `translate(0,${margin.top})`)
        .call(xAxis)
    graph.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(yAxis)

    // Animation
    bar.transition()
        .duration(800)
        .attr("width", d => x(d.freq) - x(0))
        .delay((d, i) => i * 100)
    
    // Tooltip
    let tooltip = graph.append("g")
        .append("text")
        .style("display", "none")
        .style("fill", "black")
        .style("pointer-events", "none")
        .attr("dy", -5)
        .attr("text-anchor", "middle")

    function mouseEnter(event) {
        d3.select(this).style("fill", "orange")
        tooltip.style("display", null)     
    }
    function mouseLeave(event) {
        d3.select(this).style("fill", "steelblue")
        tooltip.style("display", "none")  
    }
    function mouseMove(event, d) {
        let mouseLoc = d3.pointer(event, this)

        tooltip
            .text(d.term + ": " + d.freq.toFixed(2))
            .attr("transform",
                "translate(" + mouseLoc[0] + "," +
                (mouseLoc[1]) + ")");
    }
}
