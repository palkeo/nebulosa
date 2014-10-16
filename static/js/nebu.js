function nebu(centralword, concepts) 
{
	
		//clear the previous graph
			graph.nodeSet = {};
    		graph.nodes = [];
    		graph.edges = [];
    		graph.adjacency = {};
    		graph.notify();
				
		
		graph.addNodes(centralword);
		
		for(var i=0; i<concepts.length; i++)  //add all the nodes = all the words
		{
			graph.addNodes(concepts[i]);
			graph.addEdges([centralword, concepts[i],{color:"#6495ED"}]); //link between the nodes, color optional 
		}
		
				
		var layout = new Springy.Layout.ForceDirected(graph, 400.0, 200.0, 5.5); //change parameters of the graph 
		var renderer = new Springy.Renderer(layout,
		  function clear() {
		  },
		  function drawEdge(edge, p1, p2) {
		  },
		  function drawNode(node, p) {
		  }
		);
		
		renderer.start();
		
				jQuery(function(){
		  var springy = jQuery('#springydemo').springy({
			graph: graph
		  });
		});

}
