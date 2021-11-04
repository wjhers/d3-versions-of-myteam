
var rootWidth = 0
var rootHeight = 0
var rootLeft = 0
var rootTop = 0
var padding = {'left': 0.1, 'right': 0.1, 'top': 0.1, 'bottom': 0.1}
var timeRange = 10
var stop = false
function toggle() {
    console.log('toggle')
    stop = !stop
}

function initRootNodeSize() {
    var el=document.getElementById('treemap-canvas');
    rootWidth = +window.getComputedStyle(el,null).width.replace("px","");
    rootHeight = +window.getComputedStyle(el,null).height.replace("px","");
    rootLeft = rootWidth * padding['left']
    rootTop = rootHeight * padding['top']
    rootWidth = rootWidth - rootWidth * padding['left'] - rootWidth * padding['right']
    rootHeight = rootHeight - rootHeight * padding['top'] - rootHeight * padding['bottom']
    d3.select('#treemap-canvas').append('g')
        .attr('id', 'canvas-g')
        .attr('transform', 'translate(' + rootLeft + ',' + rootTop + ')')
}

function read_all_data(){
    let foldName = 'data'
	let filename_list = ['./' + foldName + '/agent_0_info.csv'
						,'./' + foldName + '/agent_1_info.csv'
						,'./' + foldName + '/agent_2_info.csv'
						,'./' + foldName + '/agent_3_info.csv'
						,'./' + foldName + '/agent_4_info.csv']
	let def0 = $.Deferred();
	let def1 = $.Deferred();
	let def2 = $.Deferred();
	let def3 = $.Deferred();
	let def4 = $.Deferred();
	let defer_list = [def0, def1, def2, def3, def4];

	let data_list = [];

	$.when.apply($, defer_list).then(function() {
		start_render_treemap(data_list);
	});
	
	for (let i = 0; i<filename_list.length;i++) {
		let filename = filename_list[i];
		let defer = defer_list[i];
		read_data(filename, defer, data_list);
	}
}

function read_data(filename, defer, data_list) {
	d3.csv(filename, d3.autoType)
	  .then(function(data) {
	  	data_dict = {'name': filename, 'data':data};
	  	data_list.push(data_dict);
	  	defer.resolve();
	})
}
// start rendering treemap
function start_render_treemap(data_list) {
    // initialize the global timer
    let globalTimer = {'timestep': 0}
    // render TreemapRoot node
    renderTreemapRootNode()
    // transform data_list to agents_data (determine the order)
    var agents_data = new Array(data_list.length);
    for(let i = 0; i < data_list.length; i++){
        agents_data[data_list[i]['name'].split("_")[1]] = data_list[i]['data'];
    }
    console.log('agents_data', agents_data)
    setInterval(function() {        
        render_treemap(globalTimer, agents_data)
    }, timeRange)
}

function renderTreemapRootNode() {
    // render the Root node of Treemap
    d3.select('#treemap-canvas')
        .select('#canvas-g')
        .append('rect')
        .attr('class', 'root')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', rootWidth)
        .attr('height', rootHeight)
}

function render_treemap(globalTimer, agents_data) {
    let currentTimeStep = globalTimer['timestep']
    d3.select('#treemap-canvas')
        .selectAll('.time-step-text')
        .remove()
    d3.select('#treemap-canvas')
        .append('text')
        .attr('x', 20)
        .attr('y', 100)
        .attr('class', 'time-step-text')
        .text(currentTimeStep)
    console.log('currentTimeStep', currentTimeStep)
    let DURATION = timeRange
    let agentStateList = []
    for (let i = 0; i < agents_data.length; i++) {
        agentStateList.push(agents_data[i][currentTimeStep])
    }
    let xScale = d3.scaleLinear()
        .domain([0, 400])
        .range([0, rootWidth])
    console.log(xScale(400)) 
    let yScale = d3.scaleLinear()
        .domain([0, 300])
        .range([0, rootHeight])
    console.log(yScale(300)) 
    console.log('rootWidth', rootWidth, 'rootHeight', rootHeight)
    console.log('agentStateList', agentStateList)
    let agentElement = d3.select('#treemap-canvas')
        .select('#canvas-g')
        .selectAll('.agent')
        .data(agentStateList)
        
    agentElement.enter()
        .append('rect')
        .attr('class', 'agent')
        .attr('id', function (d, i) { 
            return 'agent-' + i
        })
        .attr('x', function(d, i) {
            return xScale(d['x']-d['w'])
        })
        .attr('y', function(d, i) {
            return yScale(d['y']-d['h'])
        })
        .attr('width', function(d, i) {
            return xScale(d['w']*2)
        })
        .attr('height', function(d, i) {
            return yScale(d['h']*2)
        })
    agentElement.transition()
        .duration(DURATION)
        .attr('x', function(d, i) {
            return xScale(d['x']-d['w'])
        })
        .attr('y', function(d, i) {
            return yScale(d['y']-d['h'])
        })
        .attr('width', function(d, i) {
            return xScale(d['w']*2)
        })
        .attr('height', function(d, i) {
            return yScale(d['h']*2)
        })
    agentElement.exit().remove();
    // update the global timer 
    if (!stop) {
        globalTimer['timestep'] += 1
    }
}



initRootNodeSize()
read_all_data()
