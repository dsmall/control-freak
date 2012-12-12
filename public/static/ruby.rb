require 'capybara'
require 'date'
require 'ostruct'

# Adds helper for window.performance
# @see http://dev.w3.org/2006/webapi/WebTiming/
# {"navigation"=>{"TYPE_BACK_FORWARD"=>2'
#  "TYPE_RELOAD"=>1'
#  "redirectCount"=>0'
#  "TYPE_NAVIGATE"=>0'
#  "TYPE_RESERVED"=>255'
#  "type"=>0}'
#  "webkitNow"=>"function webkitNow() { [native code] }"'
#  "timing"=>{"fetchStart"=>1353844884946'
#  "redirectStart"=>0'
#  "domComplete"=>1353844887144'
#  "redirectEnd"=>0'
#  "loadEventStart"=>1353844887144'
#  "navigationStart"=>1353844884946'
#  "requestStart"=>1353844885033'
#  "responseEnd"=>1353844885478'
#  "secureConnectionStart"=>0'
#  "domLoading"=>1353844885359'
#  "domInteractive"=>1353844886146'
#  "domainLookupEnd"=>1353844884946'
#  "domContentLoadedEventStart"=>1353844886146'
#  "loadEventEnd"=>1353844887307'
#  "connectEnd"=>1353844885033'
#  "responseStart"=>1353844885356'
#  "unloadEventStart"=>0'
#  "domContentLoadedEventEnd"=>1353844886154'
#  "connectStart"=>1353844884994'
#  "unloadEventEnd"=>0'
#  "domainLookupStart"=>1353844884946}'
#  "memory"=>{"totalJSHeapSize"=>23100000'
#  "usedJSHeapSize"=>11900000'
#  "jsHeapSizeLimit"=>793000000}}

class PerformanceHelper
    def initialize(data)
        @data = data
    end
    
    def munge
        hash = {}
        @data.each_key do |key|
            if key == '__fxdriver_unwrapped'
                next
            end
            hash[key.to_sym] = {}
            next unless @data[key].respond_to? :each
            @data[key].each do |k,v|
                if k == '__fxdriver_unwrapped'
                    next
                end
                hash[key.to_sym][underscored(k).to_sym] = v
            end
        end
    
        hash[:summary] = {}
        hash[:summary][:redirect] = hash[:timing][:redirect_end] -
            hash[:timing][:redirect_end] if hash[:timing][:redirect_end] > 0
        hash[:summary][:app_cache] = hash[:timing][:domain_lookup_start] -
            hash[:timing][:fetch_start] if hash[:timing][:fetch_start] > 0
        hash[:summary][:dns] = hash[:timing][:domain_lookup_end] -
            hash[:timing][:domain_lookup_start] if hash[:timing][:domain_lookup_start] > 0
        hash[:summary][:tcp_connection] = hash[:timing][:connect_end] -
            hash[:timing][:connect_start] if hash[:timing][:connect_start] > 0
        hash[:summary][:tcp_connection_secure] = hash[:timing][:connect_end] -
            hash[:timing][:secure_connection_start] if 
                ((hash[:timing][:secure_connection_start] != nil) and 
                 (hash[:timing][:secure_connection_start] > 0))
        hash[:summary][:request] = hash[:timing][:response_start] -
            hash[:timing][:request_start] if hash[:timing][:request_start] > 0
        hash[:summary][:response] = hash[:timing][:response_end] -
            hash[:timing][:response_start] if hash[:timing][:response_start] > 0
        hash[:summary][:dom_processing] = hash[:timing][:dom_content_loaded_event_start] -
            hash[:timing][:dom_loading] if hash[:timing][:dom_loading] > 0
        hash[:summary][:time_to_first_byte] = hash[:timing][:response_start] -
            hash[:timing][:domain_lookup_start] if hash[:timing][:domain_lookup_start] > 0
        hash[:summary][:time_to_last_byte] = hash[:timing][:response_end] -
            hash[:timing][:domain_lookup_start] if hash[:timing][:domain_lookup_start] > 0
        hash[:summary][:response_time] = latest_timestamp(hash) - earliest_timestamp(hash)
        OpenStruct.new(hash)
    end

    private

    def underscored(camel_cased_word)
        word = camel_cased_word.to_s.dup
        word.gsub!(/::/, '/')
        word.gsub!(/([A-Z]+)([A-Z][a-z])/,'\1_\2')
        word.gsub!(/([a-z\d])([A-Z])/,'\1_\2')
        word.tr!("-", "_")
        word.downcase!
        word
    end

    def earliest_timestamp(hash)
        return hash[:timing][:navigation_start] if hash[:timing][:navigation_start] > 0
        return hash[:timing][:redirect_start] if hash[:timing][:redirect_start] > 0
        return hash[:timing][:redirect_end] if hash[:timing][:redirect_end] > 0
        return hash[:timing][:fetch_start] if hash[:timing][:fetch_start] > 0
    end

    def latest_timestamp(hash)
        return hash[:timing][:load_event_end] if hash[:timing][:load_event_end] > 0
        return hash[:timing][:load_event_start] if hash[:timing][:load_event_start] > 0
        return hash[:timing][:dom_complete] if hash[:timing][:dom_complete] > 0
        return hash[:timing][:dom_content_loaded_event_end] if hash[:timing][:dom_content_loaded_event_end] > 0
        return hash[:timing][:dom_content_loaded_event_start] if hash[:timing][:dom_content_loaded_event_start] > 0
        return hash[:timing][:dom_interactive] if hash[:timing][:dom_interactive] > 0
        return hash[:timing][:response_end] if hash[:timing][:response_end] > 0
    end
end
  
def _puts(s)
    ts = Time.now.strftime("%Y-%m-%d %H:%M:%S")
    puts "#{ts} " + s
end

puts '*** Capybara with Remote Selenium server ***'   
POS = 'ORB_H'
start = Time.now
# Today plus 3-63
checkIn = Date.today() + rand(3..63)
checkOut = checkIn + 2
_puts "INFO  - Checkin #{checkIn.strftime('%m/%d/%y')}, Checkout #{checkOut.strftime('%m/%d/%y')}"

# Capybara setup
Capybara.run_server = false
Capybara.default_wait_time = 5
Capybara.default_driver = :selenium
Capybara.register_driver :selenium do |app|
    Capybara::Selenium::Driver.new(app,
        :browser => :remote,
        :url => 'http://127.0.0.1:4444/wd/hub',
        :desired_capabilities => :chrome)
end

#  Start with home page
Capybara.app_host = 'http://www.orbitz.com'
session = Capybara::Session.new(:selenium)
_puts "INFO  - Requesting #{POS} Home page"
session.visit '/hotels/?mvt=off'
begin
    session.find(:xpath, '//meta[@name="WT.si_p"][@content="HP"]')
rescue => ex
    puts "#{ex.class}: #{ex.message}"
end

data = session.driver.evaluate_script("window.performance || window.webkitPerformance || window.mozPerformance || window.msPerformance;")
perf = PerformanceHelper.new(data).munge
# puts "TIMING:"
# perf.timing.each_pair {|key,value| puts "  #{key} => #{value}"}
puts "SUMMARY:"
perf.summary.each_pair {|key,value| puts "  #{key} => #{value/1000.0}"}
load_secs = perf.summary[:response_time]/1000.0
_puts "STATS - #{POS}_Home Time: #{load_secs} seconds."

jSessionID = session.find(:xpath, '//meta[@name=\'DCSext.wsid\']')[:content]
_puts "CHECK - JSESSIONID #{jSessionID}"

_puts "INFO  - Filling in #{POS}_Home Where, Check-in and Check-out"
session.fill_in('hotel.keyword.key', :with => 'Chicago, IL, United States')
session.fill_in('hotel.chkin', :with => checkIn.strftime('%m/%d/%y'))
session.fill_in('hotel.chkout', :with => checkOut.strftime('%m/%d/%y'))

_puts "INFO  - Clicking #{POS}_Home Search button"
session.click_on('Search')
begin
    session.find(:xpath, '//meta[@name="WT.si_p"][@content="SR"]')
rescue => ex
    puts "#{ex.class}: #{ex.message}"
end

data = session.driver.evaluate_script("window.performance || window.webkitPerformance || window.mozPerformance || window.msPerformance;")
perf = PerformanceHelper.new(data).munge
puts "SUMMARY:"
perf.summary.each_pair {|key,value| puts "  #{key} => #{value/1000.0}"}
load_secs = perf.summary[:response_time]/1000.0
_puts "STATS - #{POS}_Search Time: #{load_secs} seconds."

_puts "INFO  - Finding available hotels in #{POS}_Search results"
elements = session.all('a[@data-wt-ti="hotelCard-book"]')
hotels = elements.length
# rand returns a number >= 0 and < hotels
hotel = rand(hotels)
_puts "INFO  - Available hotels #{hotels}, chose \##{hotel+1}, clicking its Book button"
elements[hotel].click
begin
    session.find(:xpath, '//meta[@name="WT.si_p"][@content="RV"]')
rescue => ex
    puts "#{ex.class}: #{ex.message}"
end

data = session.driver.evaluate_script("window.performance || window.webkitPerformance || window.mozPerformance || window.msPerformance;")
perf = PerformanceHelper.new(data).munge
puts "SUMMARY:"
perf.summary.each_pair {|key,value| puts "  #{key} => #{value/1000.0}"}
load_secs = perf.summary[:response_time]/1000.0
_puts "STATS - #{POS}_Reprice Time: #{load_secs} seconds."

_puts "INFO  - Title \"#{session.find("head title").text}\""
# session.save_screenshot("syzygy.png")
# session.save_page("syzygy.html")

_puts "INFO  - Script elapsed #{Time.now - start} sec."

# DEBUG Let the dog see the rabbit
_puts "DEBUG - Sleep(5)"
sleep(5)

# Uncomment if local
# session.driver.browser.quit
