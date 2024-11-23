// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

contract TenisTournament {
    struct Tournament {
        string firstPlace;
        string secondPlace;
        string thirdPlace;
        string organizer;
        uint256 startDate;
        address owner;
    }

    Tournament public tournament;

    // Evento que se emitirá cuando se registren los resultados del torneo
    event TournamentResults(
        string firstPlace,
        string secondPlace,
        string thirdPlace,
		string organizer,
        uint256 startDate,
        address owner
    );

    // Función para registrar los resultados del torneo
    function setTournamentResults(
        string memory _firstPlace,
        string memory _secondPlace,
        string memory _thirdPlace,
		string memory _organizer,
        uint256 _startDate
    ) public {
        tournament = Tournament(_firstPlace, _secondPlace, _thirdPlace, _organizer, _startDate, msg.sender);
        emit TournamentResults(_firstPlace, _secondPlace, _thirdPlace, _organizer, _startDate, msg.sender);
    }

    // Función para obtener los resultados del torneo
    function getTournamentResults() public view returns (
        string memory firstPlace,
        string memory secondPlace,
        string memory thirdPlace,
		string memory organizer,
        uint256 startDate,
        address owner
    ) {
        return (
            tournament.firstPlace,
            tournament.secondPlace,
            tournament.thirdPlace,
            tournament.organizer,
            tournament.startDate,
            tournament.owner
        );
    }
}