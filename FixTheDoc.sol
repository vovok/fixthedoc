pragma solidity ^0.4.18;

contract FixTheDoc {

    string[] doc_hash;
    address public owner = msg.sender;
    modifier onlyBy(address _account)
    {
        require(msg.sender == _account);
        _;
    }

    function getLinesCount() constant public returns (uint)  {
        return doc_hash.length;
    }

    function addHash(string s) onlyBy(owner) public {
        doc_hash.push(s);
    }

    function kill() onlyBy(owner) public {
        selfdestruct(owner);
    }
}