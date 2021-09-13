
d3.csv("./data/aapl-bollinger.csv", d3.autoType)
.then(function(data) {

    console.log(data)
    console.log(data.columns)
    console.log(d3.extent(data, d => d.date))
    console.log(d3.extent(data, d => d.upper))

    margin = {top: 50, right: 50, bottom: 50, left: 50}

    //get width & height from style/css
    var el=document.getElementById('svg01');
    width = +window.getComputedStyle(el,null).width.replace("px","");
    height = +window.getComputedStyle(el,null).height.replace("px","");

    console.log(typeof width)
    console.log(height)

    x = d3.scaleUtc()
        .domain(d3.extent(data, d => d.date))
        .range([margin.left, width - margin.right])

    y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.upper)])
        .range([height - margin.bottom, margin.top])

    xAxis = g => g
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))

    yAxis = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).ticks(height / 40))
        .call(g => g.select(".domain").remove())

    //show 
    //style-1
    const line = d3.line()
        .x(d => x(d.date))
        .y(d => y(d.close))
    //style-2
    const area = d3.area()
        .x(d => x(d.date))
        .y0(y(0))
        .y1(d => y(d.close))
    //style-3
    const areaBand = d3.area()
        .x(d => x(d.date))
        .y0(d => y(d.lower))
        .y1(d => y(d.upper))
    //style-4
    const lineMiddle = d3.line()
        .x(d => x(d.date))
        .y(d => y(d.middle))



    const g_ = d3.select("#svg01").select("#g01")

    g_.select("#path01")
        .attr("d",`${area(data)}`)

    // appendix functions
    //----------------------------
    // const g_g_ = g_.select("#g01-01")

    // g_g_.attr("fill","none")
    // g_g_.attr("stroke-width","1.5")
    // g_g_.attr("stroke-miterlimit","1")

    // g_g_.append("path")
    //     .attr("id","path02")
    //     .attr("d",`${areaBand.lineY0()(data)}`)
    //     .attr("stroke","#00f")
    // g_g_.append("path")
    //     .attr("id","path03")
    //     .attr("d",`${areaBand.lineY1()(data)}`)
    //     .attr("stroke","#f00")
    //----------------------------


    g_.append("g")
        .call(xAxis).node()

    g_.append("g")
        .call(yAxis).node()

}); 

