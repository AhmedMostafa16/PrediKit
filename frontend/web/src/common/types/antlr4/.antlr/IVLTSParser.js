// Generated from ./frontend/web/src/common/types/antlr4/IVLTS.g4 by ANTLR 4.13.1
// jshint ignore: start
import antlr4 from "antlr4";
const serializedATN = [
    4, 1, 32, 295, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2, 4, 7, 4, 2, 5, 7, 5, 2, 6, 7,
    6, 2, 7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2, 10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13,
    2, 14, 7, 14, 2, 15, 7, 15, 2, 16, 7, 16, 2, 17, 7, 17, 2, 18, 7, 18, 2, 19, 7, 19, 2, 20, 7,
    20, 2, 21, 7, 21, 2, 22, 7, 22, 2, 23, 7, 23, 2, 24, 7, 24, 2, 25, 7, 25, 2, 26, 7, 26, 1, 0, 5,
    0, 56, 8, 0, 10, 0, 12, 0, 59, 9, 0, 1, 0, 1, 0, 1, 1, 5, 1, 64, 8, 1, 10, 1, 12, 1, 67, 9, 1,
    1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 3, 2, 76, 8, 2, 1, 3, 1, 3, 1, 3, 1, 3, 3, 3, 82, 8,
    3, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 3, 4, 92, 8, 4, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5,
    1, 5, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 5, 6, 106, 8, 6, 10, 6, 12, 6, 109, 9, 6, 1, 6, 3, 6,
    112, 8, 6, 5, 6, 114, 8, 6, 10, 6, 12, 6, 117, 9, 6, 1, 6, 1, 6, 1, 7, 1, 7, 3, 7, 123, 8, 7, 1,
    8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 3, 8, 137, 8, 8, 1, 9, 1,
    9, 1, 9, 1, 9, 1, 9, 1, 9, 5, 9, 145, 8, 9, 10, 9, 12, 9, 148, 9, 9, 1, 9, 3, 9, 151, 8, 9, 3,
    9, 153, 8, 9, 1, 9, 1, 9, 1, 10, 1, 10, 3, 10, 159, 8, 10, 1, 10, 1, 10, 3, 10, 163, 8, 10, 1,
    10, 1, 10, 1, 10, 1, 11, 1, 11, 1, 11, 1, 11, 1, 11, 1, 12, 1, 12, 3, 12, 175, 8, 12, 1, 13, 1,
    13, 5, 13, 179, 8, 13, 10, 13, 12, 13, 182, 9, 13, 1, 13, 1, 13, 1, 13, 1, 14, 1, 14, 1, 14, 5,
    14, 190, 8, 14, 10, 14, 12, 14, 193, 9, 14, 1, 15, 3, 15, 196, 8, 15, 1, 15, 1, 15, 1, 16, 1,
    16, 1, 16, 5, 16, 203, 8, 16, 10, 16, 12, 16, 206, 9, 16, 1, 17, 1, 17, 1, 17, 5, 17, 211, 8,
    17, 10, 17, 12, 17, 214, 9, 17, 1, 18, 1, 18, 1, 18, 5, 18, 219, 8, 18, 10, 18, 12, 18, 222, 9,
    18, 1, 19, 1, 19, 1, 19, 5, 19, 227, 8, 19, 10, 19, 12, 19, 230, 9, 19, 1, 20, 1, 20, 1, 21, 1,
    21, 1, 21, 5, 21, 237, 8, 21, 10, 21, 12, 21, 240, 9, 21, 1, 21, 3, 21, 243, 8, 21, 3, 21, 245,
    8, 21, 1, 22, 1, 22, 1, 22, 1, 22, 5, 22, 251, 8, 22, 10, 22, 12, 22, 254, 9, 22, 1, 22, 3, 22,
    257, 8, 22, 3, 22, 259, 8, 22, 1, 22, 1, 22, 1, 23, 1, 23, 1, 23, 1, 23, 1, 24, 1, 24, 1, 24, 1,
    24, 5, 24, 271, 8, 24, 10, 24, 12, 24, 274, 9, 24, 1, 24, 3, 24, 277, 8, 24, 3, 24, 279, 8, 24,
    1, 24, 1, 24, 1, 25, 1, 25, 1, 25, 1, 25, 1, 26, 1, 26, 1, 26, 5, 26, 290, 8, 26, 10, 26, 12,
    26, 293, 9, 26, 1, 26, 0, 0, 27, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32,
    34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 0, 2, 1, 0, 28, 29, 1, 0, 26, 27, 309, 0, 57, 1, 0, 0,
    0, 2, 65, 1, 0, 0, 0, 4, 75, 1, 0, 0, 0, 6, 77, 1, 0, 0, 0, 8, 83, 1, 0, 0, 0, 10, 93, 1, 0, 0,
    0, 12, 99, 1, 0, 0, 0, 14, 120, 1, 0, 0, 0, 16, 136, 1, 0, 0, 0, 18, 138, 1, 0, 0, 0, 20, 158,
    1, 0, 0, 0, 22, 167, 1, 0, 0, 0, 24, 172, 1, 0, 0, 0, 26, 176, 1, 0, 0, 0, 28, 186, 1, 0, 0, 0,
    30, 195, 1, 0, 0, 0, 32, 199, 1, 0, 0, 0, 34, 207, 1, 0, 0, 0, 36, 215, 1, 0, 0, 0, 38, 223, 1,
    0, 0, 0, 40, 231, 1, 0, 0, 0, 42, 244, 1, 0, 0, 0, 44, 246, 1, 0, 0, 0, 46, 262, 1, 0, 0, 0, 48,
    266, 1, 0, 0, 0, 50, 282, 1, 0, 0, 0, 52, 286, 1, 0, 0, 0, 54, 56, 3, 4, 2, 0, 55, 54, 1, 0, 0,
    0, 56, 59, 1, 0, 0, 0, 57, 55, 1, 0, 0, 0, 57, 58, 1, 0, 0, 0, 58, 60, 1, 0, 0, 0, 59, 57, 1, 0,
    0, 0, 60, 61, 5, 0, 0, 1, 61, 1, 1, 0, 0, 0, 62, 64, 3, 4, 2, 0, 63, 62, 1, 0, 0, 0, 64, 67, 1,
    0, 0, 0, 65, 63, 1, 0, 0, 0, 65, 66, 1, 0, 0, 0, 66, 68, 1, 0, 0, 0, 67, 65, 1, 0, 0, 0, 68, 69,
    3, 40, 20, 0, 69, 70, 5, 0, 0, 1, 70, 3, 1, 0, 0, 0, 71, 76, 3, 6, 3, 0, 72, 76, 3, 8, 4, 0, 73,
    76, 3, 10, 5, 0, 74, 76, 3, 12, 6, 0, 75, 71, 1, 0, 0, 0, 75, 72, 1, 0, 0, 0, 75, 73, 1, 0, 0,
    0, 75, 74, 1, 0, 0, 0, 76, 5, 1, 0, 0, 0, 77, 78, 5, 18, 0, 0, 78, 81, 3, 52, 26, 0, 79, 82, 5,
    1, 0, 0, 80, 82, 3, 44, 22, 0, 81, 79, 1, 0, 0, 0, 81, 80, 1, 0, 0, 0, 82, 7, 1, 0, 0, 0, 83,
    84, 5, 15, 0, 0, 84, 85, 3, 52, 26, 0, 85, 91, 3, 48, 24, 0, 86, 87, 5, 2, 0, 0, 87, 88, 3, 40,
    20, 0, 88, 89, 5, 1, 0, 0, 89, 92, 1, 0, 0, 0, 90, 92, 3, 26, 13, 0, 91, 86, 1, 0, 0, 0, 91, 90,
    1, 0, 0, 0, 92, 9, 1, 0, 0, 0, 93, 94, 5, 16, 0, 0, 94, 95, 3, 52, 26, 0, 95, 96, 5, 2, 0, 0,
    96, 97, 3, 40, 20, 0, 97, 98, 5, 1, 0, 0, 98, 11, 1, 0, 0, 0, 99, 100, 5, 19, 0, 0, 100, 101, 3,
    52, 26, 0, 101, 115, 5, 3, 0, 0, 102, 107, 3, 14, 7, 0, 103, 104, 5, 4, 0, 0, 104, 106, 3, 14,
    7, 0, 105, 103, 1, 0, 0, 0, 106, 109, 1, 0, 0, 0, 107, 105, 1, 0, 0, 0, 107, 108, 1, 0, 0, 0,
    108, 111, 1, 0, 0, 0, 109, 107, 1, 0, 0, 0, 110, 112, 5, 4, 0, 0, 111, 110, 1, 0, 0, 0, 111,
    112, 1, 0, 0, 0, 112, 114, 1, 0, 0, 0, 113, 102, 1, 0, 0, 0, 114, 117, 1, 0, 0, 0, 115, 113, 1,
    0, 0, 0, 115, 116, 1, 0, 0, 0, 116, 118, 1, 0, 0, 0, 117, 115, 1, 0, 0, 0, 118, 119, 5, 5, 0, 0,
    119, 13, 1, 0, 0, 0, 120, 122, 5, 25, 0, 0, 121, 123, 3, 44, 22, 0, 122, 121, 1, 0, 0, 0, 122,
    123, 1, 0, 0, 0, 123, 15, 1, 0, 0, 0, 124, 137, 5, 21, 0, 0, 125, 137, 5, 22, 0, 0, 126, 137, 5,
    23, 0, 0, 127, 137, 5, 24, 0, 0, 128, 137, 3, 18, 9, 0, 129, 137, 3, 22, 11, 0, 130, 137, 3, 24,
    12, 0, 131, 137, 3, 26, 13, 0, 132, 133, 5, 6, 0, 0, 133, 134, 3, 40, 20, 0, 134, 135, 5, 7, 0,
    0, 135, 137, 1, 0, 0, 0, 136, 124, 1, 0, 0, 0, 136, 125, 1, 0, 0, 0, 136, 126, 1, 0, 0, 0, 136,
    127, 1, 0, 0, 0, 136, 128, 1, 0, 0, 0, 136, 129, 1, 0, 0, 0, 136, 130, 1, 0, 0, 0, 136, 131, 1,
    0, 0, 0, 136, 132, 1, 0, 0, 0, 137, 17, 1, 0, 0, 0, 138, 139, 5, 17, 0, 0, 139, 140, 3, 40, 20,
    0, 140, 152, 5, 3, 0, 0, 141, 146, 3, 20, 10, 0, 142, 143, 5, 4, 0, 0, 143, 145, 3, 20, 10, 0,
    144, 142, 1, 0, 0, 0, 145, 148, 1, 0, 0, 0, 146, 144, 1, 0, 0, 0, 146, 147, 1, 0, 0, 0, 147,
    150, 1, 0, 0, 0, 148, 146, 1, 0, 0, 0, 149, 151, 5, 4, 0, 0, 150, 149, 1, 0, 0, 0, 150, 151, 1,
    0, 0, 0, 151, 153, 1, 0, 0, 0, 152, 141, 1, 0, 0, 0, 152, 153, 1, 0, 0, 0, 153, 154, 1, 0, 0, 0,
    154, 155, 5, 5, 0, 0, 155, 19, 1, 0, 0, 0, 156, 159, 5, 20, 0, 0, 157, 159, 3, 40, 20, 0, 158,
    156, 1, 0, 0, 0, 158, 157, 1, 0, 0, 0, 159, 162, 1, 0, 0, 0, 160, 161, 5, 14, 0, 0, 161, 163, 5,
    25, 0, 0, 162, 160, 1, 0, 0, 0, 162, 163, 1, 0, 0, 0, 163, 164, 1, 0, 0, 0, 164, 165, 5, 8, 0,
    0, 165, 166, 3, 40, 20, 0, 166, 21, 1, 0, 0, 0, 167, 168, 3, 52, 26, 0, 168, 169, 5, 6, 0, 0,
    169, 170, 3, 42, 21, 0, 170, 171, 5, 7, 0, 0, 171, 23, 1, 0, 0, 0, 172, 174, 3, 52, 26, 0, 173,
    175, 3, 44, 22, 0, 174, 173, 1, 0, 0, 0, 174, 175, 1, 0, 0, 0, 175, 25, 1, 0, 0, 0, 176, 180, 5,
    3, 0, 0, 177, 179, 3, 4, 2, 0, 178, 177, 1, 0, 0, 0, 179, 182, 1, 0, 0, 0, 180, 178, 1, 0, 0, 0,
    180, 181, 1, 0, 0, 0, 181, 183, 1, 0, 0, 0, 182, 180, 1, 0, 0, 0, 183, 184, 3, 40, 20, 0, 184,
    185, 5, 5, 0, 0, 185, 27, 1, 0, 0, 0, 186, 191, 3, 16, 8, 0, 187, 188, 5, 9, 0, 0, 188, 190, 5,
    25, 0, 0, 189, 187, 1, 0, 0, 0, 190, 193, 1, 0, 0, 0, 191, 189, 1, 0, 0, 0, 191, 192, 1, 0, 0,
    0, 192, 29, 1, 0, 0, 0, 193, 191, 1, 0, 0, 0, 194, 196, 5, 26, 0, 0, 195, 194, 1, 0, 0, 0, 195,
    196, 1, 0, 0, 0, 196, 197, 1, 0, 0, 0, 197, 198, 3, 28, 14, 0, 198, 31, 1, 0, 0, 0, 199, 204, 3,
    30, 15, 0, 200, 201, 7, 0, 0, 0, 201, 203, 3, 30, 15, 0, 202, 200, 1, 0, 0, 0, 203, 206, 1, 0,
    0, 0, 204, 202, 1, 0, 0, 0, 204, 205, 1, 0, 0, 0, 205, 33, 1, 0, 0, 0, 206, 204, 1, 0, 0, 0,
    207, 212, 3, 32, 16, 0, 208, 209, 7, 1, 0, 0, 209, 211, 3, 32, 16, 0, 210, 208, 1, 0, 0, 0, 211,
    214, 1, 0, 0, 0, 212, 210, 1, 0, 0, 0, 212, 213, 1, 0, 0, 0, 213, 35, 1, 0, 0, 0, 214, 212, 1,
    0, 0, 0, 215, 220, 3, 34, 17, 0, 216, 217, 5, 10, 0, 0, 217, 219, 3, 34, 17, 0, 218, 216, 1, 0,
    0, 0, 219, 222, 1, 0, 0, 0, 220, 218, 1, 0, 0, 0, 220, 221, 1, 0, 0, 0, 221, 37, 1, 0, 0, 0,
    222, 220, 1, 0, 0, 0, 223, 228, 3, 36, 18, 0, 224, 225, 5, 11, 0, 0, 225, 227, 3, 36, 18, 0,
    226, 224, 1, 0, 0, 0, 227, 230, 1, 0, 0, 0, 228, 226, 1, 0, 0, 0, 228, 229, 1, 0, 0, 0, 229, 39,
    1, 0, 0, 0, 230, 228, 1, 0, 0, 0, 231, 232, 3, 38, 19, 0, 232, 41, 1, 0, 0, 0, 233, 238, 3, 40,
    20, 0, 234, 235, 5, 4, 0, 0, 235, 237, 3, 40, 20, 0, 236, 234, 1, 0, 0, 0, 237, 240, 1, 0, 0, 0,
    238, 236, 1, 0, 0, 0, 238, 239, 1, 0, 0, 0, 239, 242, 1, 0, 0, 0, 240, 238, 1, 0, 0, 0, 241,
    243, 5, 4, 0, 0, 242, 241, 1, 0, 0, 0, 242, 243, 1, 0, 0, 0, 243, 245, 1, 0, 0, 0, 244, 233, 1,
    0, 0, 0, 244, 245, 1, 0, 0, 0, 245, 43, 1, 0, 0, 0, 246, 258, 5, 3, 0, 0, 247, 252, 3, 46, 23,
    0, 248, 249, 5, 4, 0, 0, 249, 251, 3, 46, 23, 0, 250, 248, 1, 0, 0, 0, 251, 254, 1, 0, 0, 0,
    252, 250, 1, 0, 0, 0, 252, 253, 1, 0, 0, 0, 253, 256, 1, 0, 0, 0, 254, 252, 1, 0, 0, 0, 255,
    257, 5, 4, 0, 0, 256, 255, 1, 0, 0, 0, 256, 257, 1, 0, 0, 0, 257, 259, 1, 0, 0, 0, 258, 247, 1,
    0, 0, 0, 258, 259, 1, 0, 0, 0, 259, 260, 1, 0, 0, 0, 260, 261, 5, 5, 0, 0, 261, 45, 1, 0, 0, 0,
    262, 263, 5, 25, 0, 0, 263, 264, 5, 12, 0, 0, 264, 265, 3, 40, 20, 0, 265, 47, 1, 0, 0, 0, 266,
    278, 5, 6, 0, 0, 267, 272, 3, 50, 25, 0, 268, 269, 5, 4, 0, 0, 269, 271, 3, 50, 25, 0, 270, 268,
    1, 0, 0, 0, 271, 274, 1, 0, 0, 0, 272, 270, 1, 0, 0, 0, 272, 273, 1, 0, 0, 0, 273, 276, 1, 0, 0,
    0, 274, 272, 1, 0, 0, 0, 275, 277, 5, 4, 0, 0, 276, 275, 1, 0, 0, 0, 276, 277, 1, 0, 0, 0, 277,
    279, 1, 0, 0, 0, 278, 267, 1, 0, 0, 0, 278, 279, 1, 0, 0, 0, 279, 280, 1, 0, 0, 0, 280, 281, 5,
    7, 0, 0, 281, 49, 1, 0, 0, 0, 282, 283, 5, 25, 0, 0, 283, 284, 5, 12, 0, 0, 284, 285, 3, 40, 20,
    0, 285, 51, 1, 0, 0, 0, 286, 291, 5, 25, 0, 0, 287, 288, 5, 13, 0, 0, 288, 290, 5, 25, 0, 0,
    289, 287, 1, 0, 0, 0, 290, 293, 1, 0, 0, 0, 291, 289, 1, 0, 0, 0, 291, 292, 1, 0, 0, 0, 292, 53,
    1, 0, 0, 0, 293, 291, 1, 0, 0, 0, 33, 57, 65, 75, 81, 91, 107, 111, 115, 122, 136, 146, 150,
    152, 158, 162, 174, 180, 191, 195, 204, 212, 220, 228, 238, 242, 244, 252, 256, 258, 272, 276,
    278, 291,
];

const atn = new antlr4.atn.ATNDeserializer().deserialize(serializedATN);

const decisionsToDFA = atn.decisionToState.map((ds, index) => new antlr4.dfa.DFA(ds, index));

const sharedContextCache = new antlr4.atn.PredictionContextCache();

export default class IVLTSParser extends antlr4.Parser {
    static grammarFileName = "IVLTS.g4";
    static literalNames = [
        null,
        "';'",
        "'='",
        "'{'",
        "','",
        "'}'",
        "'('",
        "')'",
        "'=>'",
        "'.'",
        "'&'",
        "'|'",
        "':'",
        "'::'",
        "'as'",
        "'def'",
        "'let'",
        "'match'",
        "'struct'",
        "'enum'",
        "'_'",
        null,
        null,
        null,
        null,
        null,
        "'-'",
        "'+'",
        "'*'",
        "'/'",
    ];
    static symbolicNames = [
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        "As",
        "Def",
        "Let",
        "Match",
        "Struct",
        "Enum",
        "Discard",
        "IntInterval",
        "Interval",
        "Number",
        "String",
        "Identifier",
        "OpMinus",
        "OpPlus",
        "OpMult",
        "OpDiv",
        "Space",
        "LineComment",
        "BlockComment",
    ];
    static ruleNames = [
        "definitionDocument",
        "expressionDocument",
        "definition",
        "structDefinition",
        "functionDefinition",
        "variableDefinition",
        "enumDefinition",
        "enumVariant",
        "primaryExpression",
        "matchExpression",
        "matchArm",
        "functionCall",
        "named",
        "scopeExpression",
        "fieldAccessExpression",
        "negateExpression",
        "multiplicativeExpression",
        "additiveExpression",
        "intersectionExpression",
        "unionExpression",
        "expression",
        "args",
        "fields",
        "field",
        "parameters",
        "parameter",
        "name",
    ];

    constructor(input) {
        super(input);
        this._interp = new antlr4.atn.ParserATNSimulator(
            this,
            atn,
            decisionsToDFA,
            sharedContextCache
        );
        this.ruleNames = IVLTSParser.ruleNames;
        this.literalNames = IVLTSParser.literalNames;
        this.symbolicNames = IVLTSParser.symbolicNames;
    }

    definitionDocument() {
        let localctx = new DefinitionDocumentContext(this, this._ctx, this.state);
        this.enterRule(localctx, 0, IVLTSParser.RULE_definitionDocument);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 57;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            while ((_la & ~0x1f) === 0 && ((1 << _la) & 884736) !== 0) {
                this.state = 54;
                this.definition();
                this.state = 59;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
            }
            this.state = 60;
            this.match(IVLTSParser.EOF);
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    expressionDocument() {
        let localctx = new ExpressionDocumentContext(this, this._ctx, this.state);
        this.enterRule(localctx, 2, IVLTSParser.RULE_expressionDocument);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 65;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            while ((_la & ~0x1f) === 0 && ((1 << _la) & 884736) !== 0) {
                this.state = 62;
                this.definition();
                this.state = 67;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
            }
            this.state = 68;
            this.expression();
            this.state = 69;
            this.match(IVLTSParser.EOF);
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    definition() {
        let localctx = new DefinitionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 4, IVLTSParser.RULE_definition);
        try {
            this.state = 75;
            this._errHandler.sync(this);
            switch (this._input.LA(1)) {
                case 18:
                    this.enterOuterAlt(localctx, 1);
                    this.state = 71;
                    this.structDefinition();
                    break;
                case 15:
                    this.enterOuterAlt(localctx, 2);
                    this.state = 72;
                    this.functionDefinition();
                    break;
                case 16:
                    this.enterOuterAlt(localctx, 3);
                    this.state = 73;
                    this.variableDefinition();
                    break;
                case 19:
                    this.enterOuterAlt(localctx, 4);
                    this.state = 74;
                    this.enumDefinition();
                    break;
                default:
                    throw new antlr4.error.NoViableAltException(this);
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    structDefinition() {
        let localctx = new StructDefinitionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 6, IVLTSParser.RULE_structDefinition);
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 77;
            this.match(IVLTSParser.Struct);
            this.state = 78;
            this.name();
            this.state = 81;
            this._errHandler.sync(this);
            switch (this._input.LA(1)) {
                case 1:
                    this.state = 79;
                    this.match(IVLTSParser.T__0);
                    break;
                case 3:
                    this.state = 80;
                    this.fields();
                    break;
                default:
                    throw new antlr4.error.NoViableAltException(this);
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    functionDefinition() {
        let localctx = new FunctionDefinitionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 8, IVLTSParser.RULE_functionDefinition);
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 83;
            this.match(IVLTSParser.Def);
            this.state = 84;
            this.name();
            this.state = 85;
            this.parameters();
            this.state = 91;
            this._errHandler.sync(this);
            switch (this._input.LA(1)) {
                case 2:
                    this.state = 86;
                    this.match(IVLTSParser.T__1);
                    this.state = 87;
                    this.expression();
                    this.state = 88;
                    this.match(IVLTSParser.T__0);
                    break;
                case 3:
                    this.state = 90;
                    this.scopeExpression();
                    break;
                default:
                    throw new antlr4.error.NoViableAltException(this);
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    variableDefinition() {
        let localctx = new VariableDefinitionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 10, IVLTSParser.RULE_variableDefinition);
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 93;
            this.match(IVLTSParser.Let);
            this.state = 94;
            this.name();
            this.state = 95;
            this.match(IVLTSParser.T__1);
            this.state = 96;
            this.expression();
            this.state = 97;
            this.match(IVLTSParser.T__0);
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    enumDefinition() {
        let localctx = new EnumDefinitionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 12, IVLTSParser.RULE_enumDefinition);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 99;
            this.match(IVLTSParser.Enum);
            this.state = 100;
            this.name();
            this.state = 101;
            this.match(IVLTSParser.T__2);
            this.state = 115;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            while (_la === 25) {
                this.state = 102;
                this.enumVariant();
                this.state = 107;
                this._errHandler.sync(this);
                var _alt = this._interp.adaptivePredict(this._input, 5, this._ctx);
                while (_alt != 2 && _alt != antlr4.atn.ATN.INVALID_ALT_NUMBER) {
                    if (_alt === 1) {
                        this.state = 103;
                        this.match(IVLTSParser.T__3);
                        this.state = 104;
                        this.enumVariant();
                    }
                    this.state = 109;
                    this._errHandler.sync(this);
                    _alt = this._interp.adaptivePredict(this._input, 5, this._ctx);
                }

                this.state = 111;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
                if (_la === 4) {
                    this.state = 110;
                    this.match(IVLTSParser.T__3);
                }

                this.state = 117;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
            }
            this.state = 118;
            this.match(IVLTSParser.T__4);
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    enumVariant() {
        let localctx = new EnumVariantContext(this, this._ctx, this.state);
        this.enterRule(localctx, 14, IVLTSParser.RULE_enumVariant);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 120;
            this.match(IVLTSParser.Identifier);
            this.state = 122;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            if (_la === 3) {
                this.state = 121;
                this.fields();
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    primaryExpression() {
        let localctx = new PrimaryExpressionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 16, IVLTSParser.RULE_primaryExpression);
        try {
            this.state = 136;
            this._errHandler.sync(this);
            var la_ = this._interp.adaptivePredict(this._input, 9, this._ctx);
            switch (la_) {
                case 1:
                    this.enterOuterAlt(localctx, 1);
                    this.state = 124;
                    this.match(IVLTSParser.IntInterval);
                    break;

                case 2:
                    this.enterOuterAlt(localctx, 2);
                    this.state = 125;
                    this.match(IVLTSParser.Interval);
                    break;

                case 3:
                    this.enterOuterAlt(localctx, 3);
                    this.state = 126;
                    this.match(IVLTSParser.Number);
                    break;

                case 4:
                    this.enterOuterAlt(localctx, 4);
                    this.state = 127;
                    this.match(IVLTSParser.String);
                    break;

                case 5:
                    this.enterOuterAlt(localctx, 5);
                    this.state = 128;
                    this.matchExpression();
                    break;

                case 6:
                    this.enterOuterAlt(localctx, 6);
                    this.state = 129;
                    this.functionCall();
                    break;

                case 7:
                    this.enterOuterAlt(localctx, 7);
                    this.state = 130;
                    this.named();
                    break;

                case 8:
                    this.enterOuterAlt(localctx, 8);
                    this.state = 131;
                    this.scopeExpression();
                    break;

                case 9:
                    this.enterOuterAlt(localctx, 9);
                    this.state = 132;
                    this.match(IVLTSParser.T__5);
                    this.state = 133;
                    this.expression();
                    this.state = 134;
                    this.match(IVLTSParser.T__6);
                    break;
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    matchExpression() {
        let localctx = new MatchExpressionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 18, IVLTSParser.RULE_matchExpression);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 138;
            this.match(IVLTSParser.Match);
            this.state = 139;
            this.expression();
            this.state = 140;
            this.match(IVLTSParser.T__2);
            this.state = 152;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            if ((_la & ~0x1f) === 0 && ((1 << _la) & 133300296) !== 0) {
                this.state = 141;
                this.matchArm();
                this.state = 146;
                this._errHandler.sync(this);
                var _alt = this._interp.adaptivePredict(this._input, 10, this._ctx);
                while (_alt != 2 && _alt != antlr4.atn.ATN.INVALID_ALT_NUMBER) {
                    if (_alt === 1) {
                        this.state = 142;
                        this.match(IVLTSParser.T__3);
                        this.state = 143;
                        this.matchArm();
                    }
                    this.state = 148;
                    this._errHandler.sync(this);
                    _alt = this._interp.adaptivePredict(this._input, 10, this._ctx);
                }

                this.state = 150;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
                if (_la === 4) {
                    this.state = 149;
                    this.match(IVLTSParser.T__3);
                }
            }

            this.state = 154;
            this.match(IVLTSParser.T__4);
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    matchArm() {
        let localctx = new MatchArmContext(this, this._ctx, this.state);
        this.enterRule(localctx, 20, IVLTSParser.RULE_matchArm);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 158;
            this._errHandler.sync(this);
            switch (this._input.LA(1)) {
                case 20:
                    this.state = 156;
                    this.match(IVLTSParser.Discard);
                    break;
                case 3:
                case 6:
                case 17:
                case 21:
                case 22:
                case 23:
                case 24:
                case 25:
                case 26:
                    this.state = 157;
                    this.expression();
                    break;
                default:
                    throw new antlr4.error.NoViableAltException(this);
            }
            this.state = 162;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            if (_la === 14) {
                this.state = 160;
                this.match(IVLTSParser.As);
                this.state = 161;
                this.match(IVLTSParser.Identifier);
            }

            this.state = 164;
            this.match(IVLTSParser.T__7);
            this.state = 165;
            this.expression();
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    functionCall() {
        let localctx = new FunctionCallContext(this, this._ctx, this.state);
        this.enterRule(localctx, 22, IVLTSParser.RULE_functionCall);
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 167;
            this.name();
            this.state = 168;
            this.match(IVLTSParser.T__5);
            this.state = 169;
            this.args();
            this.state = 170;
            this.match(IVLTSParser.T__6);
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    named() {
        let localctx = new NamedContext(this, this._ctx, this.state);
        this.enterRule(localctx, 24, IVLTSParser.RULE_named);
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 172;
            this.name();
            this.state = 174;
            this._errHandler.sync(this);
            var la_ = this._interp.adaptivePredict(this._input, 15, this._ctx);
            if (la_ === 1) {
                this.state = 173;
                this.fields();
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    scopeExpression() {
        let localctx = new ScopeExpressionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 26, IVLTSParser.RULE_scopeExpression);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 176;
            this.match(IVLTSParser.T__2);
            this.state = 180;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            while ((_la & ~0x1f) === 0 && ((1 << _la) & 884736) !== 0) {
                this.state = 177;
                this.definition();
                this.state = 182;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
            }
            this.state = 183;
            this.expression();
            this.state = 184;
            this.match(IVLTSParser.T__4);
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    fieldAccessExpression() {
        let localctx = new FieldAccessExpressionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 28, IVLTSParser.RULE_fieldAccessExpression);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 186;
            this.primaryExpression();
            this.state = 191;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            while (_la === 9) {
                this.state = 187;
                this.match(IVLTSParser.T__8);
                this.state = 188;
                this.match(IVLTSParser.Identifier);
                this.state = 193;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    negateExpression() {
        let localctx = new NegateExpressionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 30, IVLTSParser.RULE_negateExpression);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 195;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            if (_la === 26) {
                this.state = 194;
                this.match(IVLTSParser.OpMinus);
            }

            this.state = 197;
            this.fieldAccessExpression();
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    multiplicativeExpression() {
        let localctx = new MultiplicativeExpressionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 32, IVLTSParser.RULE_multiplicativeExpression);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 199;
            this.negateExpression();
            this.state = 204;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            while (_la === 28 || _la === 29) {
                this.state = 200;
                _la = this._input.LA(1);
                if (!(_la === 28 || _la === 29)) {
                    this._errHandler.recoverInline(this);
                } else {
                    this._errHandler.reportMatch(this);
                    this.consume();
                }
                this.state = 201;
                this.negateExpression();
                this.state = 206;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    additiveExpression() {
        let localctx = new AdditiveExpressionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 34, IVLTSParser.RULE_additiveExpression);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 207;
            this.multiplicativeExpression();
            this.state = 212;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            while (_la === 26 || _la === 27) {
                this.state = 208;
                _la = this._input.LA(1);
                if (!(_la === 26 || _la === 27)) {
                    this._errHandler.recoverInline(this);
                } else {
                    this._errHandler.reportMatch(this);
                    this.consume();
                }
                this.state = 209;
                this.multiplicativeExpression();
                this.state = 214;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    intersectionExpression() {
        let localctx = new IntersectionExpressionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 36, IVLTSParser.RULE_intersectionExpression);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 215;
            this.additiveExpression();
            this.state = 220;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            while (_la === 10) {
                this.state = 216;
                this.match(IVLTSParser.T__9);
                this.state = 217;
                this.additiveExpression();
                this.state = 222;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    unionExpression() {
        let localctx = new UnionExpressionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 38, IVLTSParser.RULE_unionExpression);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 223;
            this.intersectionExpression();
            this.state = 228;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            while (_la === 11) {
                this.state = 224;
                this.match(IVLTSParser.T__10);
                this.state = 225;
                this.intersectionExpression();
                this.state = 230;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    expression() {
        let localctx = new ExpressionContext(this, this._ctx, this.state);
        this.enterRule(localctx, 40, IVLTSParser.RULE_expression);
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 231;
            this.unionExpression();
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    args() {
        let localctx = new ArgsContext(this, this._ctx, this.state);
        this.enterRule(localctx, 42, IVLTSParser.RULE_args);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 244;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            if ((_la & ~0x1f) === 0 && ((1 << _la) & 132251720) !== 0) {
                this.state = 233;
                this.expression();
                this.state = 238;
                this._errHandler.sync(this);
                var _alt = this._interp.adaptivePredict(this._input, 23, this._ctx);
                while (_alt != 2 && _alt != antlr4.atn.ATN.INVALID_ALT_NUMBER) {
                    if (_alt === 1) {
                        this.state = 234;
                        this.match(IVLTSParser.T__3);
                        this.state = 235;
                        this.expression();
                    }
                    this.state = 240;
                    this._errHandler.sync(this);
                    _alt = this._interp.adaptivePredict(this._input, 23, this._ctx);
                }

                this.state = 242;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
                if (_la === 4) {
                    this.state = 241;
                    this.match(IVLTSParser.T__3);
                }
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    fields() {
        let localctx = new FieldsContext(this, this._ctx, this.state);
        this.enterRule(localctx, 44, IVLTSParser.RULE_fields);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 246;
            this.match(IVLTSParser.T__2);
            this.state = 258;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            if (_la === 25) {
                this.state = 247;
                this.field();
                this.state = 252;
                this._errHandler.sync(this);
                var _alt = this._interp.adaptivePredict(this._input, 26, this._ctx);
                while (_alt != 2 && _alt != antlr4.atn.ATN.INVALID_ALT_NUMBER) {
                    if (_alt === 1) {
                        this.state = 248;
                        this.match(IVLTSParser.T__3);
                        this.state = 249;
                        this.field();
                    }
                    this.state = 254;
                    this._errHandler.sync(this);
                    _alt = this._interp.adaptivePredict(this._input, 26, this._ctx);
                }

                this.state = 256;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
                if (_la === 4) {
                    this.state = 255;
                    this.match(IVLTSParser.T__3);
                }
            }

            this.state = 260;
            this.match(IVLTSParser.T__4);
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    field() {
        let localctx = new FieldContext(this, this._ctx, this.state);
        this.enterRule(localctx, 46, IVLTSParser.RULE_field);
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 262;
            this.match(IVLTSParser.Identifier);
            this.state = 263;
            this.match(IVLTSParser.T__11);
            this.state = 264;
            this.expression();
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    parameters() {
        let localctx = new ParametersContext(this, this._ctx, this.state);
        this.enterRule(localctx, 48, IVLTSParser.RULE_parameters);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 266;
            this.match(IVLTSParser.T__5);
            this.state = 278;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            if (_la === 25) {
                this.state = 267;
                this.parameter();
                this.state = 272;
                this._errHandler.sync(this);
                var _alt = this._interp.adaptivePredict(this._input, 29, this._ctx);
                while (_alt != 2 && _alt != antlr4.atn.ATN.INVALID_ALT_NUMBER) {
                    if (_alt === 1) {
                        this.state = 268;
                        this.match(IVLTSParser.T__3);
                        this.state = 269;
                        this.parameter();
                    }
                    this.state = 274;
                    this._errHandler.sync(this);
                    _alt = this._interp.adaptivePredict(this._input, 29, this._ctx);
                }

                this.state = 276;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
                if (_la === 4) {
                    this.state = 275;
                    this.match(IVLTSParser.T__3);
                }
            }

            this.state = 280;
            this.match(IVLTSParser.T__6);
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    parameter() {
        let localctx = new ParameterContext(this, this._ctx, this.state);
        this.enterRule(localctx, 50, IVLTSParser.RULE_parameter);
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 282;
            this.match(IVLTSParser.Identifier);
            this.state = 283;
            this.match(IVLTSParser.T__11);
            this.state = 284;
            this.expression();
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }

    name() {
        let localctx = new NameContext(this, this._ctx, this.state);
        this.enterRule(localctx, 52, IVLTSParser.RULE_name);
        var _la = 0;
        try {
            this.enterOuterAlt(localctx, 1);
            this.state = 286;
            this.match(IVLTSParser.Identifier);
            this.state = 291;
            this._errHandler.sync(this);
            _la = this._input.LA(1);
            while (_la === 13) {
                this.state = 287;
                this.match(IVLTSParser.T__12);
                this.state = 288;
                this.match(IVLTSParser.Identifier);
                this.state = 293;
                this._errHandler.sync(this);
                _la = this._input.LA(1);
            }
        } catch (re) {
            if (re instanceof antlr4.error.RecognitionException) {
                localctx.exception = re;
                this._errHandler.reportError(this, re);
                this._errHandler.recover(this, re);
            } else {
                throw re;
            }
        } finally {
            this.exitRule();
        }
        return localctx;
    }
}

IVLTSParser.EOF = antlr4.Token.EOF;
IVLTSParser.T__0 = 1;
IVLTSParser.T__1 = 2;
IVLTSParser.T__2 = 3;
IVLTSParser.T__3 = 4;
IVLTSParser.T__4 = 5;
IVLTSParser.T__5 = 6;
IVLTSParser.T__6 = 7;
IVLTSParser.T__7 = 8;
IVLTSParser.T__8 = 9;
IVLTSParser.T__9 = 10;
IVLTSParser.T__10 = 11;
IVLTSParser.T__11 = 12;
IVLTSParser.T__12 = 13;
IVLTSParser.As = 14;
IVLTSParser.Def = 15;
IVLTSParser.Let = 16;
IVLTSParser.Match = 17;
IVLTSParser.Struct = 18;
IVLTSParser.Enum = 19;
IVLTSParser.Discard = 20;
IVLTSParser.IntInterval = 21;
IVLTSParser.Interval = 22;
IVLTSParser.Number = 23;
IVLTSParser.String = 24;
IVLTSParser.Identifier = 25;
IVLTSParser.OpMinus = 26;
IVLTSParser.OpPlus = 27;
IVLTSParser.OpMult = 28;
IVLTSParser.OpDiv = 29;
IVLTSParser.Space = 30;
IVLTSParser.LineComment = 31;
IVLTSParser.BlockComment = 32;

IVLTSParser.RULE_definitionDocument = 0;
IVLTSParser.RULE_expressionDocument = 1;
IVLTSParser.RULE_definition = 2;
IVLTSParser.RULE_structDefinition = 3;
IVLTSParser.RULE_functionDefinition = 4;
IVLTSParser.RULE_variableDefinition = 5;
IVLTSParser.RULE_enumDefinition = 6;
IVLTSParser.RULE_enumVariant = 7;
IVLTSParser.RULE_primaryExpression = 8;
IVLTSParser.RULE_matchExpression = 9;
IVLTSParser.RULE_matchArm = 10;
IVLTSParser.RULE_functionCall = 11;
IVLTSParser.RULE_named = 12;
IVLTSParser.RULE_scopeExpression = 13;
IVLTSParser.RULE_fieldAccessExpression = 14;
IVLTSParser.RULE_negateExpression = 15;
IVLTSParser.RULE_multiplicativeExpression = 16;
IVLTSParser.RULE_additiveExpression = 17;
IVLTSParser.RULE_intersectionExpression = 18;
IVLTSParser.RULE_unionExpression = 19;
IVLTSParser.RULE_expression = 20;
IVLTSParser.RULE_args = 21;
IVLTSParser.RULE_fields = 22;
IVLTSParser.RULE_field = 23;
IVLTSParser.RULE_parameters = 24;
IVLTSParser.RULE_parameter = 25;
IVLTSParser.RULE_name = 26;

class DefinitionDocumentContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_definitionDocument;
    }

    EOF() {
        return this.getToken(IVLTSParser.EOF, 0);
    }

    definition = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(DefinitionContext);
        } else {
            return this.getTypedRuleContext(DefinitionContext, i);
        }
    };
}

class ExpressionDocumentContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_expressionDocument;
    }

    expression() {
        return this.getTypedRuleContext(ExpressionContext, 0);
    }

    EOF() {
        return this.getToken(IVLTSParser.EOF, 0);
    }

    definition = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(DefinitionContext);
        } else {
            return this.getTypedRuleContext(DefinitionContext, i);
        }
    };
}

class DefinitionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_definition;
    }

    structDefinition() {
        return this.getTypedRuleContext(StructDefinitionContext, 0);
    }

    functionDefinition() {
        return this.getTypedRuleContext(FunctionDefinitionContext, 0);
    }

    variableDefinition() {
        return this.getTypedRuleContext(VariableDefinitionContext, 0);
    }

    enumDefinition() {
        return this.getTypedRuleContext(EnumDefinitionContext, 0);
    }
}

class StructDefinitionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_structDefinition;
    }

    Struct() {
        return this.getToken(IVLTSParser.Struct, 0);
    }

    name() {
        return this.getTypedRuleContext(NameContext, 0);
    }

    fields() {
        return this.getTypedRuleContext(FieldsContext, 0);
    }
}

class FunctionDefinitionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_functionDefinition;
    }

    Def() {
        return this.getToken(IVLTSParser.Def, 0);
    }

    name() {
        return this.getTypedRuleContext(NameContext, 0);
    }

    parameters() {
        return this.getTypedRuleContext(ParametersContext, 0);
    }

    expression() {
        return this.getTypedRuleContext(ExpressionContext, 0);
    }

    scopeExpression() {
        return this.getTypedRuleContext(ScopeExpressionContext, 0);
    }
}

class VariableDefinitionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_variableDefinition;
    }

    Let() {
        return this.getToken(IVLTSParser.Let, 0);
    }

    name() {
        return this.getTypedRuleContext(NameContext, 0);
    }

    expression() {
        return this.getTypedRuleContext(ExpressionContext, 0);
    }
}

class EnumDefinitionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_enumDefinition;
    }

    Enum() {
        return this.getToken(IVLTSParser.Enum, 0);
    }

    name() {
        return this.getTypedRuleContext(NameContext, 0);
    }

    enumVariant = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(EnumVariantContext);
        } else {
            return this.getTypedRuleContext(EnumVariantContext, i);
        }
    };
}

class EnumVariantContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_enumVariant;
    }

    Identifier() {
        return this.getToken(IVLTSParser.Identifier, 0);
    }

    fields() {
        return this.getTypedRuleContext(FieldsContext, 0);
    }
}

class PrimaryExpressionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_primaryExpression;
    }

    IntInterval() {
        return this.getToken(IVLTSParser.IntInterval, 0);
    }

    Interval() {
        return this.getToken(IVLTSParser.Interval, 0);
    }

    Number() {
        return this.getToken(IVLTSParser.Number, 0);
    }

    String() {
        return this.getToken(IVLTSParser.String, 0);
    }

    matchExpression() {
        return this.getTypedRuleContext(MatchExpressionContext, 0);
    }

    functionCall() {
        return this.getTypedRuleContext(FunctionCallContext, 0);
    }

    named() {
        return this.getTypedRuleContext(NamedContext, 0);
    }

    scopeExpression() {
        return this.getTypedRuleContext(ScopeExpressionContext, 0);
    }

    expression() {
        return this.getTypedRuleContext(ExpressionContext, 0);
    }
}

class MatchExpressionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_matchExpression;
    }

    Match() {
        return this.getToken(IVLTSParser.Match, 0);
    }

    expression() {
        return this.getTypedRuleContext(ExpressionContext, 0);
    }

    matchArm = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(MatchArmContext);
        } else {
            return this.getTypedRuleContext(MatchArmContext, i);
        }
    };
}

class MatchArmContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_matchArm;
    }

    expression = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(ExpressionContext);
        } else {
            return this.getTypedRuleContext(ExpressionContext, i);
        }
    };

    Discard() {
        return this.getToken(IVLTSParser.Discard, 0);
    }

    As() {
        return this.getToken(IVLTSParser.As, 0);
    }

    Identifier() {
        return this.getToken(IVLTSParser.Identifier, 0);
    }
}

class FunctionCallContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_functionCall;
    }

    name() {
        return this.getTypedRuleContext(NameContext, 0);
    }

    args() {
        return this.getTypedRuleContext(ArgsContext, 0);
    }
}

class NamedContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_named;
    }

    name() {
        return this.getTypedRuleContext(NameContext, 0);
    }

    fields() {
        return this.getTypedRuleContext(FieldsContext, 0);
    }
}

class ScopeExpressionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_scopeExpression;
    }

    expression() {
        return this.getTypedRuleContext(ExpressionContext, 0);
    }

    definition = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(DefinitionContext);
        } else {
            return this.getTypedRuleContext(DefinitionContext, i);
        }
    };
}

class FieldAccessExpressionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_fieldAccessExpression;
    }

    primaryExpression() {
        return this.getTypedRuleContext(PrimaryExpressionContext, 0);
    }

    Identifier = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTokens(IVLTSParser.Identifier);
        } else {
            return this.getToken(IVLTSParser.Identifier, i);
        }
    };
}

class NegateExpressionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_negateExpression;
    }

    fieldAccessExpression() {
        return this.getTypedRuleContext(FieldAccessExpressionContext, 0);
    }

    OpMinus() {
        return this.getToken(IVLTSParser.OpMinus, 0);
    }
}

class MultiplicativeExpressionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_multiplicativeExpression;
    }

    negateExpression = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(NegateExpressionContext);
        } else {
            return this.getTypedRuleContext(NegateExpressionContext, i);
        }
    };

    OpMult = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTokens(IVLTSParser.OpMult);
        } else {
            return this.getToken(IVLTSParser.OpMult, i);
        }
    };

    OpDiv = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTokens(IVLTSParser.OpDiv);
        } else {
            return this.getToken(IVLTSParser.OpDiv, i);
        }
    };
}

class AdditiveExpressionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_additiveExpression;
    }

    multiplicativeExpression = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(MultiplicativeExpressionContext);
        } else {
            return this.getTypedRuleContext(MultiplicativeExpressionContext, i);
        }
    };

    OpMinus = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTokens(IVLTSParser.OpMinus);
        } else {
            return this.getToken(IVLTSParser.OpMinus, i);
        }
    };

    OpPlus = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTokens(IVLTSParser.OpPlus);
        } else {
            return this.getToken(IVLTSParser.OpPlus, i);
        }
    };
}

class IntersectionExpressionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_intersectionExpression;
    }

    additiveExpression = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(AdditiveExpressionContext);
        } else {
            return this.getTypedRuleContext(AdditiveExpressionContext, i);
        }
    };
}

class UnionExpressionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_unionExpression;
    }

    intersectionExpression = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(IntersectionExpressionContext);
        } else {
            return this.getTypedRuleContext(IntersectionExpressionContext, i);
        }
    };
}

class ExpressionContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_expression;
    }

    unionExpression() {
        return this.getTypedRuleContext(UnionExpressionContext, 0);
    }
}

class ArgsContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_args;
    }

    expression = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(ExpressionContext);
        } else {
            return this.getTypedRuleContext(ExpressionContext, i);
        }
    };
}

class FieldsContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_fields;
    }

    field = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(FieldContext);
        } else {
            return this.getTypedRuleContext(FieldContext, i);
        }
    };
}

class FieldContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_field;
    }

    Identifier() {
        return this.getToken(IVLTSParser.Identifier, 0);
    }

    expression() {
        return this.getTypedRuleContext(ExpressionContext, 0);
    }
}

class ParametersContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_parameters;
    }

    parameter = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTypedRuleContexts(ParameterContext);
        } else {
            return this.getTypedRuleContext(ParameterContext, i);
        }
    };
}

class ParameterContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_parameter;
    }

    Identifier() {
        return this.getToken(IVLTSParser.Identifier, 0);
    }

    expression() {
        return this.getTypedRuleContext(ExpressionContext, 0);
    }
}

class NameContext extends antlr4.ParserRuleContext {
    constructor(parser, parent, invokingState) {
        if (parent === undefined) {
            parent = null;
        }
        if (invokingState === undefined || invokingState === null) {
            invokingState = -1;
        }
        super(parent, invokingState);
        this.parser = parser;
        this.ruleIndex = IVLTSParser.RULE_name;
    }

    Identifier = function (i) {
        if (i === undefined) {
            i = null;
        }
        if (i === null) {
            return this.getTokens(IVLTSParser.Identifier);
        } else {
            return this.getToken(IVLTSParser.Identifier, i);
        }
    };
}

IVLTSParser.DefinitionDocumentContext = DefinitionDocumentContext;
IVLTSParser.ExpressionDocumentContext = ExpressionDocumentContext;
IVLTSParser.DefinitionContext = DefinitionContext;
IVLTSParser.StructDefinitionContext = StructDefinitionContext;
IVLTSParser.FunctionDefinitionContext = FunctionDefinitionContext;
IVLTSParser.VariableDefinitionContext = VariableDefinitionContext;
IVLTSParser.EnumDefinitionContext = EnumDefinitionContext;
IVLTSParser.EnumVariantContext = EnumVariantContext;
IVLTSParser.PrimaryExpressionContext = PrimaryExpressionContext;
IVLTSParser.MatchExpressionContext = MatchExpressionContext;
IVLTSParser.MatchArmContext = MatchArmContext;
IVLTSParser.FunctionCallContext = FunctionCallContext;
IVLTSParser.NamedContext = NamedContext;
IVLTSParser.ScopeExpressionContext = ScopeExpressionContext;
IVLTSParser.FieldAccessExpressionContext = FieldAccessExpressionContext;
IVLTSParser.NegateExpressionContext = NegateExpressionContext;
IVLTSParser.MultiplicativeExpressionContext = MultiplicativeExpressionContext;
IVLTSParser.AdditiveExpressionContext = AdditiveExpressionContext;
IVLTSParser.IntersectionExpressionContext = IntersectionExpressionContext;
IVLTSParser.UnionExpressionContext = UnionExpressionContext;
IVLTSParser.ExpressionContext = ExpressionContext;
IVLTSParser.ArgsContext = ArgsContext;
IVLTSParser.FieldsContext = FieldsContext;
IVLTSParser.FieldContext = FieldContext;
IVLTSParser.ParametersContext = ParametersContext;
IVLTSParser.ParameterContext = ParameterContext;
IVLTSParser.NameContext = NameContext;
