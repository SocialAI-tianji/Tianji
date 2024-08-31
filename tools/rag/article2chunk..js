// Updated: Aug. 20, 2024
// 运行方式: 使用 Node.js 运行此脚本。命令格式如下：
//   node testRegex.js <输入文件路径>
// 例如：
//   node testRegex.js example.txt
// 该脚本将读取指定的文本文件，并根据预定义的正则表达式模式进行处理。
// Live demo: 访问以下链接查看实时演示：
//   https://jina.ai/tokenizer
// LICENSE: 本项目采用 Apache-2.0 许可证，详情请参阅：
//   https://www.apache.org/licenses/LICENSE-2.0
// COPYRIGHT: 版权所有 (c) Jina AI

const fs = require('fs');
const util = require('util');

// Define variables for magic numbers
const MAX_HEADING_LENGTH = 7;
const MAX_HEADING_CONTENT_LENGTH = 200;
const MAX_HEADING_UNDERLINE_LENGTH = 200;
const MAX_HTML_HEADING_ATTRIBUTES_LENGTH = 100;
const MAX_LIST_ITEM_LENGTH = 200;
const MAX_NESTED_LIST_ITEMS = 6;
const MAX_LIST_INDENT_SPACES = 7;
const MAX_BLOCKQUOTE_LINE_LENGTH = 200;
const MAX_BLOCKQUOTE_LINES = 15;
const MAX_CODE_BLOCK_LENGTH = 1500;
const MAX_CODE_LANGUAGE_LENGTH = 20;
const MAX_INDENTED_CODE_LINES = 20;
const MAX_TABLE_CELL_LENGTH = 200;
const MAX_TABLE_ROWS = 20;
const MAX_HTML_TABLE_LENGTH = 2000;
const MIN_HORIZONTAL_RULE_LENGTH = 3;
const MAX_SENTENCE_LENGTH = 400;
const MAX_QUOTED_TEXT_LENGTH = 300;
const MAX_PARENTHETICAL_CONTENT_LENGTH = 200;
const MAX_NESTED_PARENTHESES = 5;
const MAX_MATH_INLINE_LENGTH = 100;
const MAX_MATH_BLOCK_LENGTH = 500;
const MAX_PARAGRAPH_LENGTH = 1000;
const MAX_STANDALONE_LINE_LENGTH = 800;
const MAX_HTML_TAG_ATTRIBUTES_LENGTH = 100;
const MAX_HTML_TAG_CONTENT_LENGTH = 1000;
const LOOKAHEAD_RANGE = 100;  // Number of characters to look ahead for a sentence boundary

const AVOID_AT_START = `[\\s\\]})>,']`;
const PUNCTUATION = `[.!?…]|\\.{3}|[\\u2026\\u2047-\\u2049]|[\\p{Emoji_Presentation}\\p{Extended_Pictographic}]`;
const QUOTE_END = `(?:'(?=\`)|''(?=\`\`))`;
const SENTENCE_END = `(?:${PUNCTUATION}(?<!${AVOID_AT_START}(?=${PUNCTUATION}))|${QUOTE_END})(?=\\S|$)`;
const SENTENCE_BOUNDARY = `(?:${SENTENCE_END}|(?=[\\r\\n]|$))`;
const LOOKAHEAD_PATTERN = `(?:(?!${SENTENCE_END}).){1,${LOOKAHEAD_RANGE}}${SENTENCE_END}`;
const NOT_PUNCTUATION_SPACE = `(?!${PUNCTUATION}\\s)`;
const SENTENCE_PATTERN = `${NOT_PUNCTUATION_SPACE}(?:[^\\r\\n]{1,{MAX_LENGTH}}${SENTENCE_BOUNDARY}|[^\\r\\n]{1,{MAX_LENGTH}}(?=${PUNCTUATION}|${QUOTE_END})(?:${LOOKAHEAD_PATTERN})?)${AVOID_AT_START}*`;


const regex = new RegExp(
    "(" +
    // 1. Headings (Setext-style, Markdown, and HTML-style, with length constraints)
    `(?:^(?:[#*=-]{1,${MAX_HEADING_LENGTH}}|\\w[^\\r\\n]{0,${MAX_HEADING_CONTENT_LENGTH}}\\r?\\n[-=]{2,${MAX_HEADING_UNDERLINE_LENGTH}}|<h[1-6][^>]{0,${MAX_HTML_HEADING_ATTRIBUTES_LENGTH}}>)[^\\r\\n]{1,${MAX_HEADING_CONTENT_LENGTH}}(?:</h[1-6]>)?(?:\\r?\\n|$))` +
    "|" +
    // New pattern for citations
    `(?:\\[[0-9]+\\][^\\r\\n]{1,${MAX_STANDALONE_LINE_LENGTH}})` +
    "|" +
    // 2. List items (bulleted, numbered, lettered, or task lists, including nested, up to three levels, with length constraints)
    `(?:(?:^|\\r?\\n)[ \\t]{0,3}(?:[-*+•]|\\d{1,3}\\.\\w\\.|\\[[ xX]\\])[ \\t]+${SENTENCE_PATTERN.replace(/{MAX_LENGTH}/g, String(MAX_LIST_ITEM_LENGTH))}` +
    `(?:(?:\\r?\\n[ \\t]{2,5}(?:[-*+•]|\\d{1,3}\\.\\w\\.|\\[[ xX]\\])[ \\t]+${SENTENCE_PATTERN.replace(/{MAX_LENGTH}/g, String(MAX_LIST_ITEM_LENGTH))}){0,${MAX_NESTED_LIST_ITEMS}}` +
    `(?:\\r?\\n[ \\t]{4,${MAX_LIST_INDENT_SPACES}}(?:[-*+•]|\\d{1,3}\\.\\w\\.|\\[[ xX]\\])[ \\t]+${SENTENCE_PATTERN.replace(/{MAX_LENGTH}/g, String(MAX_LIST_ITEM_LENGTH))}){0,${MAX_NESTED_LIST_ITEMS}})?)` +
    "|" +
    // 3. Block quotes (including nested quotes and citations, up to three levels, with length constraints)
    `(?:(?:^>(?:>|\\s{2,}){0,2}${SENTENCE_PATTERN.replace(/{MAX_LENGTH}/g, String(MAX_BLOCKQUOTE_LINE_LENGTH))}\\r?\\n?){1,${MAX_BLOCKQUOTE_LINES}})` +
    "|" +
    // 4. Code blocks (fenced, indented, or HTML pre/code tags, with length constraints)
    `(?:(?:^|\\r?\\n)(?:\`\`\`|~~~)(?:\\w{0,${MAX_CODE_LANGUAGE_LENGTH}})?\\r?\\n[\\s\\S]{0,${MAX_CODE_BLOCK_LENGTH}}?(?:\`\`\`|~~~)\\r?\\n?` +
    `|(?:(?:^|\\r?\\n)(?: {4}|\\t)[^\\r\\n]{0,${MAX_LIST_ITEM_LENGTH}}(?:\\r?\\n(?: {4}|\\t)[^\\r\\n]{0,${MAX_LIST_ITEM_LENGTH}}){0,${MAX_INDENTED_CODE_LINES}}\\r?\\n?)` +
    `|(?:<pre>(?:<code>)?[\\s\\S]{0,${MAX_CODE_BLOCK_LENGTH}}?(?:</code>)?</pre>))` +
    "|" +
    // 5. Tables (Markdown, grid tables, and HTML tables, with length constraints)
    `(?:(?:^|\\r?\\n)(?:\\|[^\\r\\n]{0,${MAX_TABLE_CELL_LENGTH}}\\|(?:\\r?\\n\\|[-:]{1,${MAX_TABLE_CELL_LENGTH}}\\|){0,1}(?:\\r?\\n\\|[^\\r\\n]{0,${MAX_TABLE_CELL_LENGTH}}\\|){0,${MAX_TABLE_ROWS}}` +
    `|<table>[\\s\\S]{0,${MAX_HTML_TABLE_LENGTH}}?</table>))` +
    "|" +
    // 6. Horizontal rules (Markdown and HTML hr tag)
    `(?:^(?:[-*_]){${MIN_HORIZONTAL_RULE_LENGTH},}\\s*$|<hr\\s*/?>)` +
    "|" +
    // 10. Standalone lines or phrases (including single-line blocks and HTML elements, with length constraints)
    `(?!${AVOID_AT_START})(?:^(?:<[a-zA-Z][^>]{0,${MAX_HTML_TAG_ATTRIBUTES_LENGTH}}>)?${SENTENCE_PATTERN.replace(/{MAX_LENGTH}/g, String(MAX_STANDALONE_LINE_LENGTH))}(?:</[a-zA-Z]+>)?(?:\\r?\\n|$))` +
    "|" +
    // 7. Sentences or phrases ending with punctuation (including ellipsis and Unicode punctuation)
    `(?!${AVOID_AT_START})${SENTENCE_PATTERN.replace(/{MAX_LENGTH}/g, String(MAX_SENTENCE_LENGTH))}` +
    "|" +
    // 8. Quoted text, parenthetical phrases, or bracketed content (with length constraints)
    "(?:" +
    `(?<!\\w)\"\"\"[^\"]{0,${MAX_QUOTED_TEXT_LENGTH}}\"\"\"(?!\\w)` +
    `|(?<!\\w)(?:['\"\`'"])[^\\r\\n]{0,${MAX_QUOTED_TEXT_LENGTH}}\\1(?!\\w)` +
    `|(?<!\\w)\`[^\\r\\n]{0,${MAX_QUOTED_TEXT_LENGTH}}'(?!\\w)` +
    `|(?<!\\w)\`\`[^\\r\\n]{0,${MAX_QUOTED_TEXT_LENGTH}}''(?!\\w)` +
    `|\\([^\\r\\n()]{0,${MAX_PARENTHETICAL_CONTENT_LENGTH}}(?:\\([^\\r\\n()]{0,${MAX_PARENTHETICAL_CONTENT_LENGTH}}\\)[^\\r\\n()]{0,${MAX_PARENTHETICAL_CONTENT_LENGTH}}){0,${MAX_NESTED_PARENTHESES}}\\)` +
    `|\\[[^\\r\\n\\[\\]]{0,${MAX_PARENTHETICAL_CONTENT_LENGTH}}(?:\\[[^\\r\\n\\[\\]]{0,${MAX_PARENTHETICAL_CONTENT_LENGTH}}\\][^\\r\\n\\[\\]]{0,${MAX_PARENTHETICAL_CONTENT_LENGTH}}){0,${MAX_NESTED_PARENTHESES}}\\]` +
    `|\\$[^\\r\\n$]{0,${MAX_MATH_INLINE_LENGTH}}\\$` +
    `|\`[^\`\\r\\n]{0,${MAX_MATH_INLINE_LENGTH}}\`` +
    ")" +
    "|" +
    // 9. Paragraphs (with length constraints)
    `(?!${AVOID_AT_START})(?:(?:^|\\r?\\n\\r?\\n)(?:<p>)?${SENTENCE_PATTERN.replace(/{MAX_LENGTH}/g, String(MAX_PARAGRAPH_LENGTH))}(?:</p>)?(?=\\r?\\n\\r?\\n|$))` +
    "|" +
    // 11. HTML-like tags and their content (including self-closing tags and attributes, with length constraints)
    `(?:<[a-zA-Z][^>]{0,${MAX_HTML_TAG_ATTRIBUTES_LENGTH}}(?:>[\\s\\S]{0,${MAX_HTML_TAG_CONTENT_LENGTH}}?</[a-zA-Z]+>|\\s*/>))` +
    "|" +
    // 12. LaTeX-style math expressions (inline and block, with length constraints)
    `(?:(?:\\$\\$[\\s\\S]{0,${MAX_MATH_BLOCK_LENGTH}}?\\$\\$)|(?:\\$[^\\$\\r\\n]{0,${MAX_MATH_INLINE_LENGTH}}\\$))` +
    "|" +
    // 14. Fallback for any remaining content (with length constraints)
    `(?!${AVOID_AT_START})${SENTENCE_PATTERN.replace(/{MAX_LENGTH}/g, String(MAX_STANDALONE_LINE_LENGTH))}` +
    ")",
    "gmu"
);


// read from the arg[1] file
const testText = fs.readFileSync(process.argv[2], 'utf8');

// Function to format bytes to a human-readable string
function formatBytes(bytes) {
    if (bytes < 1024) return bytes + " bytes";
    else if (bytes < 1048576) return (bytes / 1024).toFixed(2) + " KB";
    else if (bytes < 1073741824) return (bytes / 1048576).toFixed(2) + " MB";
    else return (bytes / 1073741824).toFixed(2) + " GB";
}

// Start measuring time and memory
const startTime = process.hrtime();
const startMemory = process.memoryUsage().heapUsed;

// Apply the regex
const matches = testText.match(regex);

// End measuring time and memory
const endTime = process.hrtime(startTime);
const endMemory = process.memoryUsage().heapUsed;

// Calculate execution time and memory usage
const executionTime = endTime[0] + endTime[1] / 1e9;
const memoryUsed = endMemory - startMemory;

// Output results
console.log(`Number of chunks: ${matches ? matches.length : 0}`);
console.log(`Execution time: ${executionTime.toFixed(3)} seconds`);
console.log(`Memory used: ${formatBytes(memoryUsed)}`);

// Output the first 5 matches (or fewer if there are less than 5)
console.log('\nFirst 10 chunks:');
if (matches) {
    matches.slice(0, 100).forEach((match, index) => {
        console.log(util.inspect(match, {maxStringLength: 50}));
    });
} else {
    console.log('No chunks found.');
}

// Output regex flags
console.log(`\nRegex flags: ${regex.flags}`);

// Check for potential issues
if (executionTime > 5) {
    console.warn('\nWarning: Execution time exceeded 5 seconds. The regex might be too complex or the input too large.');
}
if (memoryUsed > 100 * 1024 * 1024) {
    console.warn('\nWarning: Memory usage exceeded 100 MB. Consider processing the input in smaller chunks.');
}
