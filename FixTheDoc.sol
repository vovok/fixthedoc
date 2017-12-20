pragma solidity ^0.4.18;

contract FixTheDoc {

    mapping(bytes32 => bool) doc_hash;
    
    address public owner = msg.sender;

    modifier onlyBy(address _account)
    {
        require(msg.sender == _account);
        _;
    }

    function addHash(bytes32 s) onlyBy(owner) public {
        doc_hash[s] = true;
    }
    
    function checkHash(bytes32 s) constant public returns (bool) {
        return doc_hash[s];
    }

    function kill() onlyBy(owner) public {
        selfdestruct(owner);
    }
}