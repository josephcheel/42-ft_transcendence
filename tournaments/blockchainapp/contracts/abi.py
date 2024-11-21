abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "string",
				"name": "firstPlace",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "secondPlace",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "thirdPlace",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "organizer",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "startDate",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"name": "TournamentResults",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "getTournamentResults",
		"outputs": [
			{
				"internalType": "string",
				"name": "firstPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "secondPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "thirdPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "organizer",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "startDate",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_firstPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_secondPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_thirdPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_organizer",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_startDate",
				"type": "uint256"
			}
		],
		"name": "setTournamentResults",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "tournament",
		"outputs": [
			{
				"internalType": "string",
				"name": "firstPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "secondPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "thirdPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "organizer",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "startDate",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
