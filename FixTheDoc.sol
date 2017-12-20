pragma solidity ^0.4.18;

contract FixTheDoc {

    string[] doc_hash;
    address constant sender = 0xfc3234a183538515007069690f31D9cAd874D0a1;

    function getLinesCount() constant public returns (uint)  {
        return doc_hash.length;
    }

    function addHash(string s) public {
        require(msg.sender == sender);
        doc_hash.push(s);
    }
}