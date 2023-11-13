# Summary: 201 Keypoints

_(As found in Secureum's substack_ [_Security Pitfalls & Best Practices 101 Keypoints_](https://secureum.substack.com/p/security-pitfalls-and-best-practices-101) _and_ [_Security Pitfalls & Best Practices 201 Keypoints_](https://secureum.substack.com/p/security-pitfalls-and-best-practices-201)_)_

1. Solidity versions: Using very old versions of Solidity prevents benefits of bug fixes and newer security checks. Using the latest versions might make contracts susceptible to undiscovered compiler bugs. Consider using one of these versions: 0.7.5, 0.7.6 or 0.8.4 . (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#incorrect-versions-of-solidity))

2. Unlocked pragma: Contracts should be deployed using the same compiler version/flags with which they have been tested. Locking the pragma (for e.g. by not using ^ in pragma solidity 0.5.10) ensures that contracts do not accidentally get deployed using an older compiler version with unfixed bugs. (see [here](https://swcregistry.io/docs/SWC-103))

3. Multiple Solidity pragma: It is better to use one Solidity compiler version across all contracts instead of different versions with different bugs and security checks. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#different-pragma-directives-are-used))

4. Incorrect access control: Contract functions executing critical logic should have appropriate access control enforced via address checks (e.g. owner, controller etc.) typically in modifiers. Missing checks allow attackers to control critical logic. (see [here](https://docs.openzeppelin.com/contracts/3.x/api/access) and [here](https://dasp.co/#item-2))

5. Unprotected withdraw function: Unprotected (external/public) function calls sending Ether/tokens to user-controlled addresses may allow users to withdraw unauthorized funds. (see [here](https://swcregistry.io/docs/SWC-105))

6. Unprotected call to selfdestruct: A user/attacker can mistakenly/intentionally kill the contract. Protect access to such functions. (see [here](https://swcregistry.io/docs/SWC-106))

7. Modifier side-effects: Modifiers should only implement checks and not make state changes and external calls which violates the [checks-effects-interactions](https://solidity.readthedocs.io/en/develop/security-considerations.html#use-the-checks-effects-interactions-pattern) pattern. These side-effects may go unnoticed by developers/auditors because the modifier code is typically far from the function implementation. (see [here](https://consensys.net/blog/blockchain-development/solidity-best-practices-for-smart-contract-security/))

8. Incorrect modifier: If a modifier does not execute _ or revert, the function using that modifier will return the default value causing unexpected behavior. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#incorrect-modifier))

9. Constructor names: Before solc 0.4.22, constructor names had to be the same name as the contract class containing it. Misnaming it wouldn’t make it a constructor which has security implications. Solc 0.4.22 introduced the constructor keyword. Until solc 0.5.0, contracts could have both old-style and new-style constructor names with the first defined one taking precedence over the second if both existed, which also led to security issues. Solc 0.5.0 forced the use of the constructor keyword. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#multiple-constructor-schemes) and [here](https://swcregistry.io/docs/SWC-118))

10. Void constructor: Calls to base contract constructors that are unimplemented leads to misplaced assumptions. Check if the constructor is implemented or remove call if not. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#void-constructor))

11. Implicit constructor callValue check: The creation code of a contract that does not define a constructor but has a base that does, did not revert for calls with non-zero callValue when such a constructor was not explicitly payable. This is due to a compiler bug introduced in v0.4.5 and fixed in v0.6.8. Starting from Solidity 0.4.5 the creation code of contracts without explicit payable constructor is supposed to contain a callvalue check that results in contract creation reverting, if non-zero value is passed. However, this check was missing in case no explicit constructor was defined in a contract at all, but the contract has a base that does define a constructor. In these cases it is possible to send value in a contract creation transaction or using inline assembly without revert, even though the creation code is supposed to be non-payable. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

12. Controlled delegatecall: delegatecall() or callcode() to an address controlled by the user allows execution of malicious contracts in the context of the caller’s state. Ensure trusted destination addresses for such calls. (see [here](https://swcregistry.io/docs/SWC-112))

13. Reentrancy vulnerabilities: Untrusted external contract calls could callback leading to unexpected results such as multiple withdrawals or out-of-order events. Use check-effects-interactions pattern or reentrancy guards. (see [here](https://swcregistry.io/docs/SWC-107))

14. ERC777 callbacks and reentrancy: ERC777 tokens allow arbitrary callbacks via hooks that are called during token transfers. Malicious contract addresses may cause reentrancy on such callbacks if reentrancy guards are not used. (see [here](https://quantstamp.com/blog/how-the-dforce-hacker-used-reentrancy-to-steal-25-million))

15. Avoid transfer()/send() as reentrancy mitigations: Although transfer() and send() have been recommended as a security best-practice to prevent reentrancy attacks because they only forward 2300 gas, the gas repricing of opcodes may break deployed contracts. Use call() instead, without hardcoded gas limits along with checks-effects-interactions pattern or reentrancy guards for reentrancy protection. (see [here](https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/) and [here](https://swcregistry.io/docs/SWC-134))

16. Private on-chain data: Marking variables private does not mean that they cannot be read on-chain. Private data should not be stored unencrypted in contract code or state but instead stored encrypted or off-chain. (see [here](https://swcregistry.io/docs/SWC-136))

17. Weak PRNG: PRNG relying on block.timestamp, now or blockhash can be influenced by miners to some extent and should be avoided. (see [here](https://swcregistry.io/docs/SWC-120))

18. Block values as time proxies: block.timestamp and block.number are not good proxies (i.e. representations, not to be confused with smart contract proxy/implementation pattern) for time because of issues with synchronization, miner manipulation and changing block times. (see [here](https://swcregistry.io/docs/SWC-116))

19. Integer overflow/underflow: Not using OpenZeppelin’s SafeMath (or similar libraries) that check for overflows/underflows may lead to vulnerabilities or unexpected behavior if user/attacker can control the integer operands of such arithmetic operations. Solc v0.8.0 introduced default overflow/underflow checks for all arithmetic operations. (see [here](https://swcregistry.io/docs/SWC-101) and [here](https://blog.soliditylang.org/2020/10/28/solidity-0.8.x-preview/))

20. Divide before multiply: Performing multiplication before division is generally better to avoid loss of precision because Solidity integer division might truncate. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#divide-before-multiply))

21. Transaction order dependence: Race conditions can be forced on specific Ethereum transactions by monitoring the mempool. For example, the classic ERC20 approve() change can be front-run using this method. Do not make assumptions about transaction order dependence. (see [here](https://swcregistry.io/docs/SWC-114))

22. ERC20 approve() race condition: Use safeIncreaseAllowance() and safeDecreaseAllowance() from OpenZeppelin’s SafeERC20 implementation to prevent race conditions from manipulating the allowance amounts. (see [here](https://swcregistry.io/docs/SWC-114))

23. Signature malleability: The ecrecover function is susceptible to signature malleability which could lead to replay attacks. Consider using OpenZeppelin’s [ECDSA library](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol). (see [here](https://swcregistry.io/docs/SWC-117), [here](https://swcregistry.io/docs/SWC-121) and [here](https://medium.com/cryptronics/signature-replay-vulnerabilities-in-smart-contracts-3b6f7596df57))

24. ERC20 transfer() does not return boolean: Contracts compiled with solc >= 0.4.22 interacting with such functions will revert. Use OpenZeppelin’s SafeERC20 wrappers. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#incorrect-erc20-interface) and [here](https://medium.com/coinmonks/missing-return-value-bug-at-least-130-tokens-affected-d67bf08521ca))

25. Incorrect return values for ERC721 ownerOf(): Contracts compiled with solc >= 0.4.22 interacting with ERC721 ownerOf() that returns a bool instead of address type will revert. Use OpenZeppelin’s ERC721 contracts. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#incorrect-erc721-interface))

26. Unexpected Ether and this.balance: A contract can receive Ether via payable functions, selfdestruct(), coinbase transaction or pre-sent before creation. Contract logic depending on this.balance can therefore be manipulated. (see [here](https://github.com/sigp/solidity-security-blog#3-unexpected-ether-1) and [here](https://swcregistry.io/docs/SWC-132))

27. fallback vs receive(): Check that all precautions and subtleties of fallback/receive functions related to visibility, state mutability and Ether transfers have been considered.  (see [here](https://docs.soliditylang.org/en/latest/contracts.html#fallback-function) and [here](https://docs.soliditylang.org/en/latest/contracts.html#receive-ether-function))

28. Dangerous strict equalities: Use of strict equalities with tokens/Ether can accidentally/maliciously cause unexpected behavior. Consider using >= or <= instead of == for such variables depending on the contract logic. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#dangerous-strict-equalities))

29. Locked Ether: Contracts that accept Ether via payable functions but without withdrawal mechanisms will lock up that Ether. Remove payable attribute or add withdraw function. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#contracts-that-lock-ether))

30. Dangerous usage of tx.origin: Use of tx.origin for authorization may be abused by a MITM malicious contract forwarding calls from the legitimate user who interacts with it. Use msg.sender instead. (see [here](https://swcregistry.io/docs/SWC-115))

31. Contract check: Checking if a call was made from an Externally Owned Account (EOA) or a contract account is typically done using extcodesize check which may be circumvented by a contract during construction when it does not have source code available. Checking if tx.origin == msg.sender is another option. Both have implications that need to be considered. (see [here](https://consensys.net/blog/blockchain-development/solidity-best-practices-for-smart-contract-security/))

32. Deleting a mapping within a struct: Deleting a struct that contains a mapping will not delete the mapping contents which may lead to unintended consequences. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#deletion-on-mapping-containing-a-structure))

33. Tautology or contradiction: Tautologies (always true) or contradictions (always false) indicate potential flawed logic or redundant checks. e.g. x >= 0 which is always true if x is uint. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#tautology-or-contradiction))

34. Boolean constant: Use of Boolean constants (true/false) in code (e.g. conditionals) is indicative of flawed logic. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#misuse-of-a-boolean-constant))

35. Boolean equality: Boolean variables can be checked within conditionals directly without the use of equality operators to true/false. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#boolean-equality))

36. State-modifying functions: Functions that modify state (in assembly or otherwise) but are labelled constant/pure/view revert in solc >=0.5.0 (work in prior versions) because of the use of STATICCALL opcode. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#constant-functions-using-assembly-code))

37. Return values of low-level calls: Ensure that return values of low-level calls (call/callcode/delegatecall/send/etc.) are checked to avoid unexpected failures. (see [here](https://swcregistry.io/docs/SWC-104))

38. Account existence check for low-level calls: Low-level calls call/delegatecall/staticcall return true even if the account called is non-existent (per EVM design). Account existence must be checked prior to calling if needed. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#low-level-calls))

39. Dangerous shadowing: Local variables, state variables, functions, modifiers, or events with names that shadow (i.e. override) builtin Solidity symbols e.g. now or other declarations from the current scope are misleading and may lead to unexpected usages and behavior. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#builtin-symbol-shadowing))

40. Dangerous state variable shadowing: Shadowing state variables in derived contracts may be dangerous for critical variables such as contract owner (for e.g. where modifiers in base contracts check on base variables but shadowed variables are set mistakenly) and contracts incorrectly use base/shadowed variables. Do not shadow state variables. (see [here](https://swcregistry.io/docs/SWC-119))

41. Pre-declaration usage of local variables: Usage of a variable before its declaration (either declared later or in another scope) leads to unexpected behavior in solc < 0.5.0 but solc >= 0.5.0 implements C99-style scoping rules where variables can only be used after they have been declared and only in the same or nested scopes. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#pre-declaration-usage-of-local-variables))

42. Costly operations inside a loop: Operations such as state variable updates (use SSTOREs) inside a loop cost a lot of gas, are expensive and may lead to out-of-gas errors. Optimizations using local variables are preferred. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#costly-operations-inside-a-loop))

43. Calls inside a loop: Calls to external contracts inside a loop are dangerous (especially if the loop index can be user-controlled) because it could lead to DoS if one of the calls reverts or execution runs out of gas. Avoid calls within loops, check that loop index cannot be user-controlled or is bounded. (see [here](https://swcregistry.io/docs/SWC-113))

44. DoS with block gas limit: Programming patterns such as looping over arrays of unknown size may lead to DoS when the gas cost of execution exceeds the block gas limit. (see [here](https://swcregistry.io/docs/SWC-128))

45. Missing events: Events for critical state changes (e.g. owner and other critical parameters) should be emitted for tracking this off-chain. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#missing-events-access-control))

46. Unindexed event parameters: Parameters of certain events are expected to be indexed (e.g. ERC20 Transfer/Approval events) so that they’re included in the block’s bloom filter for faster access. Failure to do so might confuse off-chain tooling looking for such indexed events. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#unindexed-erc20-event-parameters))

47. Incorrect event signature in libraries: Contract types used in events in libraries cause an incorrect event signature hash. Instead of using the type `address` in the hashed signature, the actual contract name was used, leading to a wrong hash in the logs. This is due to a compiler bug introduced in v0.5.0 and fixed in v0.5.8. (see [here](https://docs.soliditylang.org/en/v0.8.1/bugs.html))

48. Dangerous unary expressions: Unary expressions such as x =+ 1 are likely errors where the programmer really meant to use x += 1. Unary + operator was deprecated in solc v0.5.0. (see [here](https://swcregistry.io/docs/SWC-129))

49. Missing zero address validation: Setters of address type parameters should include a zero-address check otherwise contract functionality may become inaccessible or tokens burnt forever. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#missing-zero-address-validation))

50. Critical address change: Changing critical addresses in contracts should be a two-step process where the first transaction (from the old/current address) registers the new address (i.e. grants ownership) and the second transaction (from the new address) replaces the old address with the new one (i.e. claims ownership). This gives an opportunity to recover from incorrect addresses mistakenly used in the first step. If not, contract functionality might become inaccessible. (see [here](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/1488) and [here](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/2369))

51. assert()/require() state change: Invariants in assert() and require() statements should not modify the state per best practices. (see [here](https://swcregistry.io/docs/SWC-110))

52. require() vs assert(): require() should be used for checking error conditions on inputs and return values while assert() should be used for invariant checking. Between solc 0.4.10 and 0.8.0, require() used REVERT (0xfd) opcode which refunded remaining gas on failure while assert() used INVALID (0xfe) opcode which consumed all the supplied gas. (see [here](https://docs.soliditylang.org/en/v0.8.1/control-structures.html#error-handling-assert-require-revert-and-exceptions))

53. Deprecated keywords: Use of deprecated functions/operators such as block.blockhash() for blockhash(), msg.gas for gasleft(), throw for revert(), sha3() for keccak256(), callcode() for delegatecall(), suicide() for selfdestruct(), constant for view or var for actual type name should be avoided to prevent unintended errors with newer compiler versions. (see [here](https://swcregistry.io/docs/SWC-111))

54. Function default visibility: Functions without a visibility type specifier are public by default in solc < 0.5.0. This can lead to a vulnerability where a malicious user may make unauthorized state changes. solc >= 0.5.0 requires explicit function visibility specifiers. (see [here](https://swcregistry.io/docs/SWC-100))

55. Incorrect inheritance order: Contracts inheriting from multiple contracts with identical functions should specify the correct inheritance order i.e. more general to more specific to avoid inheriting the incorrect function implementation. (see [here](https://swcregistry.io/docs/SWC-125))

56. Missing inheritance: A contract might appear (based on name or functions implemented) to inherit from another interface or abstract contract without actually doing so. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#missing-inheritance))

57. Insufficient gas griefing: Transaction relayers need to be trusted to provide enough gas for the transaction to succeed. (see [here](https://swcregistry.io/docs/SWC-126))

58. Modifying reference type parameters: Structs/Arrays/Mappings passed as arguments to a function may be by value (memory) or reference (storage) as specified by the data location (optional before solc 0.5.0). Ensure correct usage of memory and storage in function parameters and make all data locations explicit. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#modifying-storage-array-by-value))

59. Arbitrary jump with function type variable: Function type variables should be carefully handled and avoided in assembly manipulations to prevent jumps to arbitrary code locations. (see [here](https://swcregistry.io/docs/SWC-127))

60. Hash collisions with multiple variable length arguments: Using abi.encodePacked() with multiple variable length arguments can, in certain situations, lead to a hash collision. Do not allow users access to parameters used in abi.encodePacked(), use fixed length arrays or use abi.encode(). (see [here](https://swcregistry.io/docs/SWC-133) and [here](https://docs.soliditylang.org/en/v0.5.3/abi-spec.html#non-standard-packed-mode))

61. Malleability risk from dirty high order bits: Types that do not occupy the full 32 bytes might contain “dirty higher order bits” which does not affect operation on types but gives different results with msg.data. (see [here](https://docs.soliditylang.org/en/v0.8.1/security-considerations.html#minor-details))

62. Incorrect shift in assembly: Shift operators (shl(x, y), shr(x, y), sar(x, y)) in Solidity assembly apply the shift operation of x bits on y and not the other way around, which may be confusing. Check if the values in a shift operation are reversed. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#incorrect-shift-in-assembly))

63. Assembly usage: Use of EVM assembly is error-prone and should be avoided or double-checked for correctness. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#assembly-usage))

64. Right-To-Left-Override control character (U+202E): Malicious actors can use the Right-To-Left-Override unicode character to force RTL text rendering and confuse users as to the real intent of a contract. U+202E character should not appear in the source code of a smart contract. (see [here](https://swcregistry.io/docs/SWC-130))

65. Constant state variables: Constant state variables should be declared constant to save gas. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#state-variables-that-could-be-declared-constant))

66. Similar variable names: Variables with similar names could be confused for each other and therefore should be avoided. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#variable-names-too-similar))

67. Uninitialized state/local variables: Uninitialized state/local variables are assigned zero values by the compiler and may cause unintended results e.g. transferring tokens to zero address. Explicitly initialize all state/local variables. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#uninitialized-state-variables) and [here](https://github.com/crytic/slither/wiki/Detector-Documentation#uninitialized-local-variables))

68. Uninitialized storage pointers: Uninitialized local storage variables can point to unexpected storage locations in the contract, which can lead to vulnerabilities. Solc 0.5.0 and above disallow such pointers. (see [here](https://swcregistry.io/docs/SWC-109))

69. Uninitialized function pointers in constructors: Calling uninitialized function pointers in constructors of contracts compiled with solc versions 0.4.5-0.4.25 and 0.5.0-0.5.7 lead to unexpected behavior because of a compiler bug. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#uninitialized-function-pointers-in-constructors))

70. Long number literals: Number literals with many digits should be carefully checked as they are prone to error. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#too-many-digits))

71. Out-of-range enum: Solc < 0.4.5 produced unexpected behavior with out-of-range enums. Check enum conversion or use a newer compiler. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#dangerous-enum-conversion))

72. Uncalled public functions: Public functions that are never called from within the contracts should be declared external to save gas. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#public-function-that-could-be-declared-external))

73. Dead/Unreachable code: Dead code may be indicative of programmer error, missing logic or potential optimization opportunity, which needs to be flagged for removal or addressed appropriately. (see [here](https://en.wikipedia.org/wiki/Dead_code))

74. Unused return values: Unused return values of function calls are indicative of programmer errors which may have unexpected behavior. (see [here](https://github.com/crytic/slither/wiki/Detector-Documentation#unused-return))

75. Unused variables: Unused state/local variables may be indicative of programmer error, missing logic or potential optimization opportunity, which needs to be flagged for removal or addressed appropriately. (see [here](https://swcregistry.io/docs/SWC-131))

76. Redundant statements: Statements with no effects that do not produce code may be indicative of programmer error or missing logic, which needs to be flagged for removal or addressed appropriately. (see [here](https://swcregistry.io/docs/SWC-135))

77. Storage array with signed Integers with ABIEncoderV2: Assigning an array of signed integers to a storage array of different type can lead to data corruption in that array. This is due to a compiler bug introduced in v0.4.7 and fixed in v0.5.10. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html)) 

78. Dynamic constructor arguments clipped with ABIEncoderV2: A contract's constructor which takes structs or arrays that contain dynamically sized arrays reverts or decodes to invalid data when ABIEncoderV2 is used. This is due to a compiler bug introduced in v0.4.16 and fixed in v0.5.9. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

79. Storage array with multiSlot element with ABIEncoderV2: Storage arrays containing structs or other statically sized arrays are not read properly when directly encoded in external function calls or in abi.encode(). This is due to a compiler bug introduced in v0.4.16 and fixed in v0.5.10. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

80. Calldata structs with statically sized and dynamically encoded members with ABIEncoderV2: Reading from calldata structs that contain dynamically encoded, but statically sized members can result in incorrect values. This is due to a compiler bug introduced in v0.5.6 and fixed in v0.5.11. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

81. Packed storage with ABIEncoderV2: Storage structs and arrays with types shorter than 32 bytes can cause data corruption if encoded directly from storage using ABIEncoderV2. This is due to a compiler bug introduced in v0.5.0 and fixed in v0.5.7. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

82. Incorrect loads with Yul optimizer and ABIEncoderV2: The Yul optimizer incorrectly replaces MLOAD and SLOAD calls with values that have been previously written to the load location. This can only happen if ABIEncoderV2 is activated and the experimental Yul optimizer has been activated manually in addition to the regular optimizer in the compiler settings. This is due to a compiler bug introduced in v0.5.14 and fixed in v0.5.15. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

83. Array slice dynamically encoded base type with ABIEncoderV2: Accessing array slices of arrays with dynamically encoded base types (e.g. multi-dimensional arrays) can result in invalid data being read. This is due to a compiler bug introduced in v0.6.0 and fixed in v0.6.8. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

84. Missing escaping in formatting with ABIEncoderV2: String literals containing double backslash characters passed directly to external or encoding function calls can lead to a different string being used when ABIEncoderV2 is enabled. This is due to a compiler bug introduced in v0.5.14 and fixed in v0.6.8. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

85. Double shift size overflow: Double bitwise shifts by large constants whose sum overflows 256 bits can result in unexpected values. Nested logical shift operations whose total shift size is 2**256 or more are incorrectly optimized. This only applies to shifts by numbers of bits that are compile-time constant expressions. This happens when the optimizer is used and evmVersion >= Constantinople. This is due to a compiler bug introduced in v0.5.5 and fixed in v0.5.6. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

86. Incorrect byte instruction optimization: The optimizer incorrectly handles byte opcodes whose second argument is 31 or a constant expression that evaluates to 31. This can result in unexpected values. This can happen when performing index access on bytesNN types with a compile time constant value (not index) of 31 or when using the byte opcode in inline assembly. This is due to a compiler bug introduced in v0.5.5 and fixed in v0.5.7. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

87. Essential assignments removed with Yul Optimizer : The Yul optimizer can remove essential assignments to variables declared inside for loops when Yul's continue or break statement is used mostly while using inline assembly with for loops and continue and break statements. This is due to a compiler bug introduced in v0.5.8/v0.6.0 and fixed in v0.5.16/v0.6.1. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

88. Private methods overridden: While private methods of base contracts are not visible and cannot be called directly from the derived contract, it is still possible to declare a function of the same name and type and thus change the behaviour of the base contract's function. This is due to a compiler bug introduced in v0.3.0 and fixed in v0.5.17. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

89. Tuple assignment multi stack slot components: Tuple assignments with components that occupy several stack slots, i.e. nested tuples, pointers to external functions or references to dynamically sized calldata arrays, can result in invalid values. This is due to a compiler bug introduced in v0.1.6 and fixed in v0.6.6. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

90. Dynamic array cleanup: When assigning a dynamically sized array with types of size at most 16 bytes in storage causing the assigned array to shrink, some parts of deleted slots were not zeroed out. This is due to a compiler bug fixed in v0.7.3. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

91. Empty byte array copy: Copying an empty byte array (or string) from memory or calldata to storage can result in data corruption if the target array's length is increased subsequently without storing new data. This is due to a compiler bug fixed in v0.7.4. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

92. Memory array creation overflow: The creation of very large memory arrays can result in overlapping memory regions and thus memory corruption. This is due to a compiler bug introduced in v0.2.0 and fixed in v0.6.5. (see [here](https://solidity.ethereum.org/2020/04/06/memory-creation-overflow-bug/))

93. Calldata using for: Function calls to internal library functions with calldata parameters called via “using for” can result in invalid data being read. This is due to a compiler bug introduced in v0.6.9 and fixed in v0.6.10. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

94. Free function redefinition: The compiler does not flag an error when two or more free functions (functions outside of a contract) with the same name and parameter types are defined in a source unit or when an imported free function alias shadows another free function with a different name but identical parameter types. This is due to a compiler bug introduced in v0.7.1 and fixed in v0.7.2. (see [here](https://docs.soliditylang.org/en/v0.8.9/bugs.html))

95. Unprotected initializers in proxy-based upgradeable contracts: Proxy-based upgradeable contracts need to use public initializer functions instead of constructors that need to be explicitly called only once. Preventing multiple invocations of such initializer functions (e.g. via initializer modifier from OpenZeppelin’s Initializable library) is a must. (see [here](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#initializers) and [here](https://github.com/crytic/slither/wiki/Upgradeability-Checks#initializer-is-not-called))

96. Initializing state-variables in proxy-based upgradeable contracts: This should be done in initializer functions and not as part of the state variable declarations in which case they won’t be set. (see [here](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#avoid-initial-values-in-field-declarations))

97. Import upgradeable contracts in proxy-based upgradeable contracts: Contracts imported from proxy-based upgradeable contracts should also be upgradeable where such contracts have been modified to use initializers instead of constructors. (see [here](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#use-upgradeable-libraries))

98. Avoid selfdestruct or delegatecall in proxy-based upgradeable contracts: This will cause the logic contract to be destroyed and all contract instances will end up delegating calls to an address without any code. (see [here](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#potentially-unsafe-operations))

99. State variables in proxy-based upgradeable contracts: The declaration order/layout and type/mutability of state variables in such contracts should be preserved exactly while upgrading to prevent critical storage layout mismatch errors. (see [here](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#modifying-your-contracts))

100. Function ID collision between proxy/implementation in proxy-based upgradeable contracts: Malicious proxy contracts may exploit function ID collision to invoke unintended proxy functions instead of delegating to implementation functions. Check for function ID collisions. (see [here](https://github.com/crytic/slither/wiki/Upgradeability-Checks#functions-ids-collisions) and [here](https://forum.openzeppelin.com/t/beware-of-the-proxy-learn-how-to-exploit-function-clashing/1070))

101. Function shadowing between proxy/contract in proxy-based upgradeable contracts: Shadow functions in proxy contract prevent functions in logic contract from being invoked. (see [here](https://github.com/crytic/slither/wiki/Upgradeability-Checks#functions-shadowing))

102. ERC20 transfer and transferFrom: Should return a boolean. Several tokens do not return a boolean on these functions. As a result, their calls in the contract might fail. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#erc-conformity))

103. ERC20 name, decimals, and symbol functions: Are present if used. These functions are optional in the ERC20 standard and might not be present. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#erc-conformity))

104. ERC20 decimals returns a uint8: Several tokens incorrectly return a uint256. If this is the case, ensure the value returned is below 255. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#erc-conformity))

105. ERC20 approve race-condition: The ERC20 standard has a known ERC20 race condition that must be mitigated to prevent attackers from stealing tokens. (see [here](https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729))

106. ERC777 hooks: ERC777 tokens have the concept of a hook function that is called before any calls to send, transfer, operatorSend, minting and burning. While these hooks enable a lot of interesting use cases, care should be taken to make sure they do not make external calls because that can lead to reentrancies. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#erc-conformity))

107. Token Deflation via fees: Transfer and transferFrom should not take a fee. Deflationary tokens can lead to unexpected behavior. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#erc-conformity))

108. Token Inflation via interest: Potential interest earned from the token should be taken into account. Some tokens distribute interest to token holders. This interest might be trapped in the contract if not taken into account. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#erc-conformity))

109. Token contract avoids unneeded complexity: The token should be a simple contract; a token with complex code requires a higher standard of review. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#contract-composition))

110. Token contract has only a few non–token-related functions: Non–token-related functions increase the likelihood of an issue in the contract. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#contract-composition))

111. Token only has one address: Tokens with multiple entry points for balance updates can break internal bookkeeping based on the address (e.g. balances[token_address][msg.sender] might not reflect the actual balance). (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#contract-composition))

112. Token is not upgradeable: Upgradeable contracts might change their rules over time. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#owner-privileges))

113. Token owner has limited minting capabilities: Malicious or compromised owners can abuse minting capabilities. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#owner-privileges))

114. Token is not pausable: Malicious or compromised owners can trap contracts relying on pausable tokens. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#owner-privileges))

115. Token owner cannot blacklist the contract: Malicious or compromised owners can trap contracts relying on tokens with a blacklist. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#owner-privileges))

116. Token development team is known and can be held responsible for abuse: Contracts with anonymous development teams, or that reside in legal shelters should require a higher standard of review. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#owner-privileges))

117. No token user owns most of the supply: If a few users own most of the tokens, they can influence operations based on the token's repartition. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#token-scarcity))

118. Token total supply is sufficient: Tokens with a low total supply can be easily manipulated. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#token-scarcity))

119. Tokens are located in more than a few exchanges: If all the tokens are in one exchange, a compromise of the exchange can compromise the contract relying on the token. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#token-scarcity))

120. Token balance and Flash loans: Users understand the associated risks of large funds or flash loans. Contracts relying on the token balance must carefully take in consideration attackers with large funds or attacks through flash loans. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#token-scarcity))

121. Token does not allow flash minting: Flash minting can lead to substantial swings in the balance and the total supply, which necessitate strict and comprehensive overflow checks in the operation of the token. (see [here](https://github.com/crytic/building-secure-contracts/blob/master/development-guidelines/token_integration.md#token-scarcity))

122. ERC1400 permissioned addresses: Can block transfers from/to specific addresses. (see [here](https://gist.github.com/shayanb/cd495e23c7cf1a8b269f8ce7fd198538#file-token_checklist-md))

123. ERC1400 forced transfers: Trusted actors have the ability to transfer funds however they choose. (see [here](https://gist.github.com/shayanb/cd495e23c7cf1a8b269f8ce7fd198538#file-token_checklist-md))

124. ERC1644 forced transfers: Controller has the ability to steal funds. (see [here](https://gist.github.com/shayanb/cd495e23c7cf1a8b269f8ce7fd198538#file-token_checklist-md))

125. ERC621 control of totalSupply: totalSupply can be changed by trusted actors (see [here](https://gist.github.com/shayanb/cd495e23c7cf1a8b269f8ce7fd198538#file-token_checklist-md))

126. ERC884 cancel and reissue: Token implementers have the ability to cancel an address and move its tokens to a new address (see [here](https://gist.github.com/shayanb/cd495e23c7cf1a8b269f8ce7fd198538#file-token_checklist-md))

127. ERC884 whitelisting: Tokens can only be sent to whitelisted addresses (see [here](https://gist.github.com/shayanb/cd495e23c7cf1a8b269f8ce7fd198538#file-token_checklist-md))

128. Guarded launch via asset limits: Limiting the total asset value managed by a system initially upon launch and gradually increasing it over time may reduce impact due to initial vulnerabilities or exploits. (see [here](https://medium.com/electric-capital/derisking-defi-guarded-launches-2600ce730e0a#:~:text=Guarded%20Launches:%20Protecting%20Users%20with%20Limits&text=A%20new%20contract%20is%20deployed,product%20in%20a%20limited%20scope.))

129. Guarded launch via asset types: Limiting types of assets that can be used in the protocol initially upon launch and gradually expanding to other assets over time may reduce impact due to initial vulnerabilities or exploits. (see [here](https://medium.com/electric-capital/derisking-defi-guarded-launches-2600ce730e0a#:~:text=Guarded%20Launches:%20Protecting%20Users%20with%20Limits&text=A%20new%20contract%20is%20deployed,product%20in%20a%20limited%20scope.))

130. Guarded launch via user limits: Limiting the total number of users that can interact with a system initially upon launch and gradually increasing it over time may reduce impact due to initial vulnerabilities or exploits. Initial users may also be whitelisted to limit to trusted actors before opening the system to everyone. (see [here](https://medium.com/electric-capital/derisking-defi-guarded-launches-2600ce730e0a#:~:text=Guarded%20Launches:%20Protecting%20Users%20with%20Limits&text=A%20new%20contract%20is%20deployed,product%20in%20a%20limited%20scope.))

131. Guarded launch via usage limits: Enforcing transaction size limits, daily volume limits, per-account limits, or rate-limiting transactions may reduce impact due to initial vulnerabilities or exploits. (see [here](https://medium.com/electric-capital/derisking-defi-guarded-launches-2600ce730e0a#:~:text=Guarded%20Launches:%20Protecting%20Users%20with%20Limits&text=A%20new%20contract%20is%20deployed,product%20in%20a%20limited%20scope.))

132. Guarded launch via composability limits: Restricting the composability of the system to interface only with whitelisted trusted contracts before expanding to arbitrary external contracts may reduce impact due to initial vulnerabilities or exploits. (see [here](https://medium.com/electric-capital/derisking-defi-guarded-launches-2600ce730e0a#:~:text=Guarded%20Launches:%20Protecting%20Users%20with%20Limits&text=A%20new%20contract%20is%20deployed,product%20in%20a%20limited%20scope.))

133. Guarded launch via escrows: Escrowing high value transactions/operations with time locks and a governance capability to nullify or revert transactions may reduce impact due to initial vulnerabilities or exploits. (see [here](https://medium.com/electric-capital/derisking-defi-guarded-launches-2600ce730e0a#:~:text=Guarded%20Launches:%20Protecting%20Users%20with%20Limits&text=A%20new%20contract%20is%20deployed,product%20in%20a%20limited%20scope.))

134. Guarded launch via circuit breakers: Implementing capabilities to pause/unpause a system in extreme scenarios may reduce impact due to initial vulnerabilities or exploits. (see [here](https://medium.com/electric-capital/derisking-defi-guarded-launches-2600ce730e0a#:~:text=Guarded%20Launches:%20Protecting%20Users%20with%20Limits&text=A%20new%20contract%20is%20deployed,product%20in%20a%20limited%20scope.))

135. Guarded launch via emergency shutdown: Implement capabilities that allow governance to shutdown new activity in the system and allow users to reclaim assets may reduce impact due to initial vulnerabilities or exploits. (see [here](https://medium.com/electric-capital/derisking-defi-guarded-launches-2600ce730e0a#:~:text=Guarded%20Launches:%20Protecting%20Users%20with%20Limits&text=A%20new%20contract%20is%20deployed,product%20in%20a%20limited%20scope.))

136. System specification: Ensure that the specification of the entire system is considered, written and evaluated to the greatest detail possible. Specification describes how (and why) the different components of the system behave to achieve the design requirements. Without specification, a system implementation cannot be evaluated against the requirements for correctness.

137. System documentation: Ensure that roles, functionalities and interactions of the entire system are well documented to the greatest detail possible. Documentation describes what (and how) the implementation of different components of the system does to achieve the specification goals. Without documentation, a system implementation cannot be evaluated against the specification for correctness and one will have to rely on analyzing the implementation itself.

138. Function parameters: Ensure input validation for all function parameters especially if the visibility is external/public where (untrusted) users can control values. This is especially required for address parameters where maliciously/accidentally used incorrect/zero addresses can cause vulnerabilities or unexpected behavior.

139. Function arguments: Ensure that the arguments to function calls at the caller sites are the correct ones and in the right order as expected by the function definition.

140. Function visibility: Ensure that the strictest visibility is used for the required functionality. An accidental external/public visibility will allow (untrusted) users to invoke functionality that is supposed to be restricted internally.

141. Function modifiers: Ensure that the right set of function modifiers are used (in the correct order) for the specific functions so that the expected access control or validation is correctly enforced.

142. Function return values: Ensure that the appropriate return value(s) are returned from functions and checked without ignoring at function call sites, so that error conditions are caught and handled appropriately.

143. Function invocation timeliness: Externally accessible functions (external/public visibility) may be called at any time (or never). It is not safe to assume they will only be called at specific system phases (e.g. after initialization, when unpaused, during liquidation) that is meaningful to the system design. The reason for this can be accidental or malicious. Function implementation should be robust enough to track system state transitions, determine meaningful states for invocations and withstand arbitrary calls. For e.g., initialization functions (used with upgradeable contracts that cannot use constructors) are meant to be called atomically along with contract deployment to prevent anyone else from initializing with arbitrary values.

144. Function invocation repetitiveness: Externally accessible functions (external/public visibility) may be called any number of times. It is not safe to assume they will only be called only once or a specific number of times that is meaningful to the system design. Function implementation should be robust enough to track, prevent, ignore or account for arbitrarily repetitive invocations. For e.g., initialization functions (used with upgradeable contracts that cannot use constructors) are meant to be called only once.

145. Function invocation order:  Externally accessible functions (external/public visibility) may be called in any order (with respect to other defined functions). It is not safe to assume they will only be called in the specific order that makes sense to the system design or is implicitly assumed in the code. For e.g., initialization functions (used with upgradeable contracts that cannot use constructors) are meant to be called before other system functions can be called.

146. Function invocation arguments: Externally accessible functions (external/public visibility) may be called with any possible arguments. Without complete and proper validation (e.g. zero address checks, bound checks, threshold checks etc.), they cannot be assumed to comply with any assumptions made about them in the code.

147. Conditionals: Ensure that in conditional expressions (e.g. if statements), the correct variables are being checked and the correct operators, if any, are being used to combine them. For e.g. using || instead of && is a common error.

148. Access control specification: Ensure that the various system actors, their access control privileges and trust assumptions are accurately specified in great detail so that they are correctly implemented and enforced across different contracts, functions and system transitions/flows.

149. Access control implementation: Ensure that the specified access control is implemented uniformly across all the subjects (actors) seeking access and objects (variables, functions) being accessed so that there are no paths/flows where the access control is missing or may be side-stepped.

150. Missing modifiers: Access control is typically enforced on functions using modifiers that check if specific addresses/roles are calling these functions. Ensure that such modifiers are present on all relevant functions which require that specific access control.

151. Incorrectly implemented modifiers: Access control is typically enforced on functions using modifiers that check if specific addresses/roles are calling these functions. A system can have multiple roles with different privileges. Ensure that modifiers are implementing the expected checks on the correct roles/addresses with the right composition e.g. incorrect use of || instead of && is a common vulnerability while composing access checks.

152. Incorrectly used modifiers: Access control is typically enforced on functions using modifiers that check if specific addresses/roles are calling these functions. A system can have multiple roles with different privileges. Ensure that correct modifiers are used on functions requiring specific access control enforced by that modifier.

153. Access control changes: Ensure that changes to access control (e.g. change of ownership to new addresses) are handled with extra security so that such transitions happen smoothly without contracts getting locked out or compromised due to use of incorrect credentials.

154. Comments: Ensure that the code is well commented both with NatSpec and inline comments for better readability and maintainability. The comments should accurately reflect what the corresponding code does. Stale comments should be removed. Discrepancies between code and comments should be addressed. Any TODO’s indicated by comments should be addressed. Commented code should be removed.

155. Tests: Tests indicate that the system implementation has been validated against the specification. Unit tests, functional tests and integration tests should have been performed to achieve good test coverage across the entire codebase. Any code or parameterisation used specifically for testing should be removed from production code.

156. Unused constructs: Any unused imports, inherited contracts, functions, parameters, variables, modifiers, events or return values should be removed (or used appropriately) after careful evaluation. This will not only reduce gas costs but improve readability and maintainability of the code.

157. Redundant constructs: Redundant code and comments can be confusing and should be removed (or changed appropriately) after careful evaluation. This will not only reduce gas costs but improve readability and maintainability of the code.

158. ETH Handling: Contracts that accept/manage/transfer ETH should ensure that functions handling ETH are using msg.value appropriately, logic that depends on ETH value accounts for less/more ETH sent, logic that depends on contract ETH balance accounts for the different direct/indirect (e.g. coinbase transaction, selfdestruct recipient) ways of receiving ETH and transfers are reentrancy safe. Functions handling ETH should be checked extra carefully for access control, input validation and error handling.

159. Token Handling: Contracts that accept/manage/transfer ERC tokens should ensure that functions handling tokens account for different types of ERC tokens (e.g. ERC20 vs ERC777), deflationary/inflationary tokens, rebasing tokens and trusted/external tokens. Functions handling tokens should be checked extra carefully for access control, input validation and error handling.

160. Trusted actors: Ideally there should be no trusted actors while interacting with smart contracts. However, in guarded launch scenarios, the goal is to start with trusted actors and then progressively decentralise towards automated governance by community/DAO. For the trusted phase, all the trusted actors, their roles and capabilities should be clearly specified, implemented accordingly and documented for user information and examination.

161. Privileged roles and EOAs: Trusted actors who have privileged roles with capabilities to deploy contracts, change critical parameters, pause/unpause system, trigger emergency shutdown, withdraw/transfer/drain funds and allow/deny other actors should be addresses controlled by multiple, independent, mutually distrusting entities. They should not be controlled by private keys of EOAs but with Multisigs with a high threshold (e.g. 5-of-7, 9-of-11) and eventually by a DAO of token holders. EOA has a single point of failure.

162. Two-step change of privileged roles: When privileged roles are being changed, it is recommended to follow a two-step approach: 1) The current privileged role proposes a new address for the change 2) The newly proposed address then claims the privileged role in a separate transaction. This two-step change allows accidental proposals to be corrected instead of leaving the system operationally with no/malicious privileged role. For e.g., in a single-step change, if the current admin accidentally changes the new admin to a zero-address or an incorrect address (where the private keys are not available), the system is left without an operational admin and will have to be redeployed.

163. Time-delayed change of critical parameters: When critical parameters of systems need to be changed, it is required to broadcast the change via event emission and recommended to enforce the changes after a time-delay. This is to allow system users to be aware of such critical changes and give them an opportunity to exit or adjust their engagement with the system accordingly. For e.g. reducing the rewards or increasing the fees in a system might not be acceptable to some users who may wish to withdraw their funds and exit.

164. Explicit over Implicit: While Solidity has progressively adopted explicit declarations of intent for e.g. with function visibility and variable storage, it is recommended to do the same at the application level where all requirements should be explicitly validated (e.g. input parameters) and assumptions should be documented and checked. Implicit requirements and assumptions should be flagged as dangerous.

165. Configuration issues: Misconfiguration of system components such contracts, parameters, addresses and permissions may lead to security issues.

166. Initialization issues: Lack of initialization, initializing with incorrect values or allowing untrusted actors to initialize system parameters may lead to security issues.

167. Cleanup issues: Missing to clean up old state or cleaning up incorrectly/insufficiently will lead to reuse of stale state which may lead to security issues.

168. Data processing issues: Processing data incorrectly will cause unexpected behavior which may lead to security issues.

169. Data validation issues: Missing validation of data or incorrectly/insufficiently validating data, especially tainted data from untrusted users, will cause untrustworthy system behavior which may lead to security issues.

170. Numerical issues: Incorrect numerical computation will cause unexpected behavior which may lead to security issues.

171. Accounting issues: Incorrect or insufficient tracking or accounting of business logic related aspects such as states, phases, permissions, roles, funds (deposits/withdrawals) and tokens (mints/burns/transfers) may lead to security issues.

172. Access control issues: Incorrect or insufficient access control or authorization related to system actors, roles, assets and permissions may lead to security issues.

173. Auditing/logging issues: Incorrect or insufficient emission of events will impact off-chain monitoring and incident response capabilities which may lead to security issues.

174. Cryptography issues: Incorrect or insufficient cryptography especially related to on-chain signature verification or off-chain key management will impact access control and may lead to security issues.

175. Error-reporting issues: Incorrect or insufficient detecting, reporting and handling of error conditions will cause exceptional behavior to go unnoticed which may lead to security issues.

176. Denial-of-Service (DoS) issues: Preventing other users from successfully accessing system services by modifying system parameters or state causes denial-of-service issues which affects the availability of the system. This may also manifest as security issues if users are not able to access their funds locked in the system.

177. Timing issues: Incorrect assumptions on timing of user actions, system state transitions or blockchain state/blocks/transactions may lead to security issues.

178. Ordering issues: Incorrect assumptions on ordering of user actions or system state transitions may lead to security issues. For e.g.,  a user may accidentally/maliciously call a finalization function even before the initialization function if the system allows.

179. Undefined behavior issues: Any behavior that is undefined in the specification but is allowed in the implementation will result in unexpected outcomes which may lead to security issues.

180. External interaction issues: Interacting with external components (e.g. tokens, contracts, oracles) forces system to trust or make assumptions on their correctness/availability requiring validation of their existence and outputs without which may lead to security issues.

181. Trust issues: Incorrect or Insufficient trust assumption about/among system actors and external entities will lead to privilege escalation/abuse which may lead to security issues.

182. Gas issues: Incorrect assumptions about gas requirements especially for loops or external calls will lead to out-of-gas exceptions which may lead to security issues such as failed transfers or locked funds.

183. Dependency issues: Dependencies on external actors or software (imports, contracts, libraries, tokens etc.) will lead to trust/availability/correctness assumptions which if/when broken may lead to security issues.

184. Constant issues: Incorrect assumptions about system actors, entities or parameters being constant may lead to security issues if/when such factors change unexpectedly.

185. Freshness issues: Incorrect assumptions about the status of or data from system actors or entities being fresh (i.e. not stale), because of lack of updation or availability, may lead to security issues if/when such factors have been updated. For e.g., getting a stale price from an Oracle.

186. Scarcity issues: Incorrect assumptions about the scarcity of tokens/funds available to any system actor will lead to unexpected outcomes which may lead to security issues. For e.g., flash loans.

187. Incentive issues: Incorrect assumptions about the incentives of system/external actors to perform or not perform certain actions will lead to unexpected behavior being triggered or expected behavior not being triggered, both of which may lead to security issues. For e.g., incentive to liquidate positions, lack of incentive to DoS or grief system.

188. Clarity issues: Lack of clarity in system specification, documentation, implementation or UI/UX will lead to incorrect expectations/outcome which may lead to security issues.

189. Privacy issues: Data and transactions on the Ethereum blockchain are not private. Anyone can observe contract state and track transactions (both included in a block and pending in the mempool). Incorrect assumptions about privacy aspects of data or transactions can be abused which may lead to security issues.

190. Cloning issues: Copy-pasting code from other libraries, contracts or even different parts of the same contract may result in incorrect code semantics for the context being copied to, copy over any vulnerabilities or miss any security fixes applied to the original code. All these may lead to security issues. 

191. Business logic issues: Incorrect or insufficient assumptions about the higher-order business logic being implemented in the application will lead to differences in expected and actual behavior, which may result in security issues.

192. Principle of Least Privilege: “Every program and every user of the system should operate using the least set of privileges necessary to complete the job” — Ensure that various system actors have the least amount of privilege granted as required by their roles to execute their specified tasks. Granting excess privilege is prone to misuse/abuse when trusted actors misbehave or their access is hijacked by malicious entities. (See [Saltzer and Schroeder's Secure Design Principles](https://en.wikipedia.org/wiki/Saltzer_and_Schroeder's_design_principles))

193. Principle of Separation of Privilege: “Where feasible, a protection mechanism that requires two keys to unlock it is more robust and flexible than one that allows access to the presenter of only a single key” — Ensure that critical privileges are separated across multiple actors so that there are no single points of failure/abuse. A good example of this is to require a multisig address (not EOA) for privileged actors (e.g. owner, admin, governor, deployer) who control key contract functionality such as pause/unpause/shutdown, emergency fund drain, upgradeability, allow/deny list and critical parameters. The multisig address should be composed of entities that are different and mutually distrusting/verifying. (See [Saltzer and Schroeder's Secure Design Principles](https://en.wikipedia.org/wiki/Saltzer_and_Schroeder's_design_principles))

194. Principle of Least Common Mechanism: “Minimize the amount of mechanism common to more than one user and depended on by all users” — Ensure that only the least number of security-critical modules/paths as required are shared amongst the different actors/code so that impact from any vulnerability/compromise in shared components is limited and contained to the smallest possible subset. (See [Saltzer and Schroeder's Secure Design Principles](https://en.wikipedia.org/wiki/Saltzer_and_Schroeder's_design_principles))

195. Principle of Fail-safe Defaults: “Base access decisions on permission rather than exclusion” — Ensure that variables or permissions are initialized to fail-safe default values which can be made more inclusive later instead of opening up the system to everyone including untrusted actors. (See [Saltzer and Schroeder's Secure Design Principles](https://en.wikipedia.org/wiki/Saltzer_and_Schroeder's_design_principles))

196. Principle of Complete Mediation: “Every access to every object must be checked for authority.” — Ensure that any required access control is enforced along all access paths to the object or function being protected. (See [Saltzer and Schroeder's Secure Design Principles](https://en.wikipedia.org/wiki/Saltzer_and_Schroeder's_design_principles))

197. Principle of Economy of Mechanism: “Keep the design as simple and small as possible” — Ensure that contracts and functions are not overly complex or large so as to reduce readability or maintainability. Complexity typically leads to insecurity. (See [Saltzer and Schroeder's Secure Design Principles](https://en.wikipedia.org/wiki/Saltzer_and_Schroeder's_design_principles))

198. Principle of Open Design: “The design should not be secret” — Smart contracts are expected to be open-sourced and accessible to everyone. Security by obscurity of code or underlying algorithms is not an option. Security should be derived from the strength of the design and implementation under the assumption that (byzantine) attackers will study their details and try to exploit them in arbitrary ways. (See [Saltzer and Schroeder's Secure Design Principles](https://en.wikipedia.org/wiki/Saltzer_and_Schroeder's_design_principles))

199. Principle of Psychological Acceptability: “It is essential that the human interface be designed for ease of use, so that users routinely and automatically apply the protection mechanisms correctly” — Ensure that security aspects of smart contract interfaces and system designs/flows are user-friendly and intuitive so that users can interact with minimal risk. (See [Saltzer and Schroeder's Secure Design Principles](https://en.wikipedia.org/wiki/Saltzer_and_Schroeder's_design_principles))

200. Principle of Work Factor: “Compare the cost of circumventing the mechanism with the resources of a potential attacker” — Given the magnitude of value managed by smart contracts, it is safe to assume that byzantine attackers will risk the greatest amounts of intellectual/financial/social capital possible to subvert such systems. Therefore, the mitigation mechanisms must factor in the highest levels of risk. (See [Saltzer and Schroeder's Secure Design Principles](https://en.wikipedia.org/wiki/Saltzer_and_Schroeder's_design_principles))

201. Principle of Compromise Recording: “Mechanisms that reliably record that a compromise of information has occurred can be used in place of more elaborate mechanisms that completely prevent loss” — Ensure that smart contracts and their accompanying operational infrastructure can be monitored/analyzed at all times (development/deployment/runtime) for minimizing loss from any compromise due to vulnerabilities/exploits. For e.g., critical operations in contracts should necessarily emit events to facilitate monitoring at runtime. (See [Saltzer and Schroeder's Secure Design Principles](https://en.wikipedia.org/wiki/Saltzer_and_Schroeder's_design_principles))