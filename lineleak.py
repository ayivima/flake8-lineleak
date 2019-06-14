
"""(c) Copyright 2019, Victor Mawusi Ayi."""

from tokenize import (
    COMMENT,
    ENDMARKER,
    NEWLINE,
    NL,
    OP,
    STRING,
)

import attr


__name__ = "flake8-lineleak"
__version__ = "1.0.2"


# Warnings & Messages
LLI200 = (
    "LLI200 [INFO] Live code count: "
    "{} logical and {} physical lines."
)

LLW404 = (
    "LLW404 Maximum number of logical live "
    "code lines ({}) exceeded."
)

LLW405 = (
    "LLW405 Maximum number of physical "
    "live code lines ({}) exceeded."
)


@attr.s
class Screener():
    """Core class of lineleak.

    Counts live code lines and sends warning or statistics to flake8.
    """

    name = __name__
    version = __version__

    BLACKLIST = []
    LIVE_CODE_COUNT = False
    LOGICAL = False
    MAX_LINE_COUNT = 100

    tree = attr.ib(default=None)
    file_tokens = attr.ib(factory=list)
    filename = attr.ib(default=None)

    def analyse(self):
        """Count live code lines, and get first line which exceeds limit."""
        limit_reached = False
        physical_line_deductions = 0
        prev_line_no = None
        log_line_count = 0
        leak_line = None
        prev_token_type = None

        for token_type, token_value, start, end, _line in self.file_tokens:

            start_line_num = start[0]
            end_line_num, end_line_end = end
            phy_line_count = start_line_num - physical_line_deductions

            # making necessary adjustments for physical
            # and logical line counts exclude blank lines
            # and comments from count.
            if token_type == NEWLINE:
                log_line_count += 1

            elif (
                (token_type == NL and start_line_num != prev_line_no)
                or token_type == COMMENT
                or token_type == ENDMARKER
            ):
                physical_line_deductions += 1

            # exclude docstrings from count
            elif (
                token_type == STRING
                and token_value.startswith(('"""', "'''"))
                and prev_token_type != OP
            ):
                log_line_count -= 1
                if end_line_num == start_line_num:
                    physical_line_deductions += 1
                else:
                    physical_line_deductions += (
                        end_line_num - start_line_num + 1
                    )

            # checking for leak line while limit is not reached.
            # check stops if limit has been reached
            if not limit_reached:
                if (
                    (log_line_count > self.MAX_LINE_COUNT and self.LOGICAL)
                    or (
                        phy_line_count > self.MAX_LINE_COUNT
                        and not self.LOGICAL
                    ) and token_type not in (NL, COMMENT, STRING)
                ):
                    limit_reached = True
                    leak_line = start_line_num

            prev_token_type = token_type
            prev_line_no = start_line_num

        last_line, last_cell = end_line_num, end_line_end
        logical_line_count = log_line_count

        physical_line_count = (
            last_line - physical_line_deductions
        )

        return (
            last_cell,
            last_line,
            leak_line,
            limit_reached,
            logical_line_count,
            physical_line_count
        )

    @classmethod
    def add_options(cls, parser):
        """Register optional arguments."""
        parser.add_option(
            "--lineleak-ignore", default="",
            parse_from_config=False, comma_separated_list=True,
            help="Specifies files leakline must ignore."
        )

        parser.add_option(
            "--lineleak-logical", action="store_true",
            parse_from_config=False,
            help="Applies line count limit to logical lines."
        )

        parser.add_option(
            "--live-code-count", action="store_true",
            parse_from_config=False,
            help="Displays the number of physical"
                 "and logical lines containing live code."
        )

        parser.add_option(
            "--max-line-count", type=int,
            parse_from_config=False,
            help="Changes the maximum limit for live code line count."
        )

    @classmethod
    def parse_options(cls, options):
        """Parse command-line arguments."""
        if options.lineleak_ignore:
            cls.BLACKLIST = options.lineleak_ignore

        if options.live_code_count:
            cls.LIVE_CODE_COUNT = True
            # No need to continue through function,
            # if only count of lines of live code requested
            return None

        if options.lineleak_logical:
            cls.LOGICAL = True

        if options.max_line_count:
            cls.MAX_LINE_COUNT = options.max_line_count

    def run(self):
        """Run check, and send the relevant message or warning to flake8."""
        if self.filename in self.BLACKLIST:
            pass
        else:
            (
                last_cell,
                last_line,
                leak_line,
                limit_reached,
                logical_line_count,
                physical_line_count
            ) = self.analyse()

            if self.LIVE_CODE_COUNT:
                # requesting live code count overrides limit check
                # and displays the number of live code lines
                yield (
                    last_line, last_cell,
                    LLI200.format(
                        logical_line_count,
                        physical_line_count
                    ), type(self)
                )
            else:
                leak_warning = LLW404 if self.LOGICAL else LLW405

                if limit_reached:
                    yield (
                        leak_line, 0,
                        leak_warning.format(self.MAX_LINE_COUNT),
                        type(self)
                    )
