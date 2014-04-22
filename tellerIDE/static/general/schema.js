var state = stately(

{
	loaded:"boolean",

	database_name: "string",
	visualizer_mode: "string",

	editor: {
		tabs: [{body:"string", name: "string"}],
		current_tab: "number"
	},

	history: {
		queries: [{query:"string", result: "string"}],
		current_query: "number"
	},

	mutation: {
		mutations: [{
			value: "string",
			target: "string",
			makes_new_tab: "boolean",
			name: "string",
			description: "string"
		}],
		current_mutation: "number"
	},

	framing: {
		central: "number",
		left: "number",
		right: "number"
	},

	settings: {
		prompt_for_tab_name: "boolean"
	}

}


);

state().settings().prompt_for_tab_name(false);