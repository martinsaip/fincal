# Financial Calendar

Market holidays and trading hours.

## How do I get it?

Install with npm:

    npm install fincal

Clone repo with git:

    git clone https://github.com/triploc/fincal.git

Download over HTTPS:

    wget https://github.com/triploc/fincal/archive/master.zip
    unzip master.zip

## How do I use it?

    var fincal = require("fincal");
    
    // New York (NYSE)
    fincal.new_york.time();
    fincal.new_york.isEquityMarketHoliday();
    fincal.new_york.isEquityMarketPartialTradingDay();
    fincal.new_york.areEquityMarketsOpen();
    
    // London (LSE)
    fincal.london.time();
    fincal.london.areEquityMarketsOpen();
    
    // Paris (Euronext)
    fincal.paris.time();
    fincal.paris.areEquityMarketsOpen();
    
    // Frankfurt
    fincal.frankfurt.time();
    fincal.frankfurt.areEquityMarketsOpen();
    
    // Hong Kong
    fincal.hong_kong.time();
    fincal.hong_kong.areEquityMarketsOpen();
    
    // Shanghai
    fincal.shanghai.time();
    fincal.shanghai.areEquityMarketsOpen();
    
    // Tokyo
    fincal.tokyo.time();
    fincal.tokyo.areEquityMarketsOpen();
    
    // Syndey
    fincal.sydney.time();
    fincal.sydney.areEquityMarketsOpen();

## License

Copyright (c) 2015, Jonathan Hollinger

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.