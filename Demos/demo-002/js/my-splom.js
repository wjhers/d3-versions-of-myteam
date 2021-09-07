// Refer to https://observablehq.com/@d3/brushable-scatterplot-matrix
let species = 'Class'
let sepal_length = 'Sepal Length'
d3.csv('./data/Iris.csv', d3.autoType) // https://github.com/d3/d3-dsv#autoType
  .then(function(data) {
    console.log('data: ', data);

    let columns = data.columns.filter(d => d !== species)
    let width = 964
    let padding = 20
    let size = (width - (columns.length + 1) * padding) / columns.length + padding
    let x = columns.map(c => d3.scaleLinear()
      .domain(d3.extent(data, d => d[c]))
      .rangeRound([padding / 2, size - padding / 2]))
    let y = x.map(x => x.copy().range([size - padding / 2, padding / 2]))
    let z = d3.scaleOrdinal()
      .domain(data.map(d => d[species]))
      .range(d3.schemeCategory10)

    // handle xAixis
    let xAxis = (g)=>{
      const axis = d3.axisBottom()
        .ticks(6)
        .tickSize(size * columns.length);
      return g.selectAll("g").data(x).join("g")
        .attr("transform", (d, i) => `translate(${i * size},0)`)
        .each(function(d) { return d3.select(this).call(axis.scale(d)); })
        .call(g => g.select(".domain").remove())
        .call(g => {
          g.selectAll(".tick line").attr("stroke", "#ddd")
          .attr('y1', size * columns.length)
        });
    }

    // handle yAixis
    let yAxis = (g)=>{
      const axis = d3.axisLeft()
        .ticks(6)
        .tickSize(-size * columns.length);
      return g.selectAll("g").data(y).join("g")
        .attr("transform", (d, i) => `translate(0,${i * size})`)
        .each(function(d) { return d3.select(this).call(axis.scale(d)); })
        .call(g => g.select(".domain").remove())
        .call(g => {
          g.selectAll(".tick line").attr("stroke", "#ddd")
            .attr('x2', 0)
        });
    }

    const svg = d3.select("#svg-data")
      .attr("viewBox", [-padding, 0, width, width]);

    svg.append("style")
      .text(`circle.hidden { fill: #000; fill-opacity: 1; r: 1px; }`);

    let g_xAxis = svg.append("g")
      .attr('class', 'xAxis')
      .call(xAxis);

    let g_yAxis = svg.append("g")
      .attr('class', 'yAxis')
      .call(yAxis);

    const cell = svg.append("g")
      .attr('class', 'gCell')
      .selectAll("g")
      .data(d3.cross(d3.range(columns.length), d3.range(columns.length)))
      .join("g")
        .attr("transform", ([i, j]) => `translate(${i * size},${j * size})`);

    // show rect border
    cell.append("rect")
      .attr("fill", "none")
      .attr("stroke", "#aaa")
      .attr("x", padding / 2 + 0.5)
      .attr("y", padding / 2 + 0.5)
      .attr("width", size - padding)
      .attr("height", size - padding);

    let t_duration = 1000

    // draw circles in each cell
    cell.each(function([i, j]) {
      d3.select(this).selectAll("circle")
        .data(data)
        .join("circle")
        .attr('cx', size/2)
        .attr('cy', size/2)
        .transition().duration(t_duration)
          .attr("cx", d => x[i](d[columns[i]]))
          .attr("cy", d => y[j](d[columns[j]]))
    });

    // animation to draw grid lines
    g_xAxis
      .transition().duration(t_duration + 50)
      .on('end', function() { // https://github.com/d3/d3-transition/blob/v1.2.0/README.md#control-flow
        d3.select(this).selectAll('.tick line')
          .transition().duration(t_duration * 2)
          .attr('y1', 0)
      })

    g_yAxis
      .transition().duration(t_duration+ 50)
      .on('end', function() {
        d3.select(this).selectAll('.tick line')
          .transition().duration(t_duration * 2)
          .attr('x2', size * columns.length)
      })

    const circle = cell.selectAll("circle")
      .attr("r", 3.5)
      .attr("fill-opacity", 0.7)
      .attr("fill", d => z(d[species]));

    // brush
    cell.call(brush, circle);

    svg.append("g")
      .style("font", "bold 10px sans-serif")
      .style("pointer-events", "none")
      .selectAll("text")
      .data(columns)
      .join("text")
        .attr("transform", (d, i) => `translate(${i * size},${i * size})`)
        .attr("x", padding)
        .attr("y", padding)
        .attr("dy", ".71em")
        .text(d => d);

    function brush(cell, circle) {
      const brush = d3.brush()
        .extent([[padding / 2, padding / 2], [size - padding / 2, size - padding / 2]])
        .on("start", brushstarted)
        .on("brush", brushed)
        .on("end", brushended);

      cell.call(brush);

      let brushCell;

      // Clear the previously-active brush, if any.
      function brushstarted() {
        if (brushCell !== this) {
          d3.select(brushCell).call(brush.move, null);
          brushCell = this;
        }
      }

      // Highlight the selected circles.
      function brushed([i, j]) {
        if (d3.event.selection == null) return;
        const [[x0, y0], [x1, y1]] = d3.event.selection;
        circle.classed("hidden", 
          d => x0 > x[i](d[columns[i]])
            || x1 < x[i](d[columns[i]])
            || y0 > y[j](d[columns[j]])
            || y1 < y[j](d[columns[j]]));
        let selected = []
        selected = data.filter(
          d => x0 < x[i](d[columns[i]])
            && x1 > x[i](d[columns[i]])
            && y0 < y[j](d[columns[j]])
            && y1 > y[j](d[columns[j]]));
        console.log("selected:",selected);
        // cleanSvgChart(); //using transition().duration()
        drawChart(selected);
      }

      // If the brush is empty, select all circles.
      function brushended([i, j]) {
        if (d3.event.selection != null){
          return;
        }
        circle.classed("hidden", false);
      }
    }
  }
)

function cleanSvgChart(){
  d3.select("#svg-chart").selectAll('*').remove();
}

function drawChart(items){
  let margin = {top:20, right:20, bottom:30, left:25}
  let width = 390
  let height = 400
  let color = "steelblue"
  let data1 = items.map(d => d[sepal_length])
  let draw_data = Object.assign(data1,{x: "SL/CM", y:"Counts/N"})
  let draw_bin = d3.histogram().thresholds(7)(draw_data)
  
  console.log("000-draw_bin",draw_bin);

  function deleteUndifinedX0(draw_bin){
    for(var i=draw_bin.length-1;i>=0;i--){
      if(typeof(draw_bin[i].x0)==="undefined" || typeof(draw_bin[i].x1)==="undefined"){
        draw_bin.splice(i,1)
      }
    }
  }
  deleteUndifinedX0(draw_bin)
  console.log("001-draw_bin",draw_bin);

  // if(draw_bin.length === 1){
  //   draw_bin[0]['x1'] = draw_bin[0]['0'] + 0.02;
  //   console.log("-------",draw_bin)
  // }
  
  if(draw_bin.length !== 0){ //There has some data in Array draw_bin
  let x_ = d3.scaleLinear()
    .domain([draw_bin[0].x0, draw_bin[draw_bin.length-1].x1])
    .rangeRound([margin.left, width-margin.right])

  let y_ = d3.scaleLinear()
    .domain([0,d3.max(draw_bin,d=>d.length)]).nice()
    .range([height-margin.bottom,margin.top])    

  let xAxis_ = g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x_).ticks(width / 80 ).tickSizeOuter(0))
    .call(g => g.append("text")
      .attr("x", width - 1.6*margin.right)
      .attr("y", 15)
      .attr("fill", "currentColor")
      .attr("font-weight", "bold")
      .attr("text-anchor", "start")
      .text(draw_data.x))

  let yAxis_ = g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y_).ticks(height / 40))
    .call(g => g.select(".domain").remove())
    .call(g => g.select(".tick:last-of-type text").clone()
      .attr("x", 0)
      .attr("y", 10)
      .attr("text-anchor", "end")
      .attr("transform","rotate(-90)")
      .attr("font-weight", "bold")
      .text(draw_data.y))

  // function deleteUndifinedX0(draw_bin){
  //   for(var i=draw_bin.length-1;i>=0;i--){
  //     if(typeof(draw_bin[i].x0)==="undefined" || typeof(draw_bin[i].x1)==="undefined"){
  //       draw_bin.splice(i,1)
  //     }
  //   }
  // }
  // deleteUndifinedX0(draw_bin)
  // console.log("draw_bin",draw_bin);

  const svg_ = d3.select("#svg-chart")
    .attr("viewBox", [0, 0, width, height]);

  const t = svg_.transition()
    .duration(750)

  svg_.select("#svg-chart-g")
    .selectAll(".histogram-bar")
    .data(draw_bin)
    .join(
      enter => enter.append("rect")
        .attr('class', 'histogram-bar')
        .attr("x", d => x_(d.x0) + 1)
        .attr("width", d => Math.max(0, x_(d.x1) - x_(d.x0) - 1))
        .attr("y", d => y_(d.length))
        .attr("height", d => y_(0) - y_(d.length)),
      update => update
        .call(update => update.transition(t)
        .attr("x", d => x_(d.x0) + 1)
        .attr("width", d => Math.max(0, x_(d.x1) - x_(d.x0) - 1))
        .attr("y", d => y_(d.length))
        .attr("height", d => y_(0) - y_(d.length))),
      exit => exit
        .remove()
    )

  d3.select("#svg-chart-xaxis").selectAll('*').remove();
  d3.select("#svg-chart-yaxis").selectAll('*').remove();

  svg_.select("#svg-chart-xaxis")
    .call(xAxis_);

  svg_.select("#svg-chart-yaxis")
    .call(yAxis_);
  }

}