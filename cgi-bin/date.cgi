#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
typename Date = [|Date:(Int,Int)|];
typename BookingInfo = (person:String, age:Int, arrival:Date, departure:Date);

sig date : Formlet(Date)
var date = 
  formlet
   <#>
     { inputInt -> day } / { inputInt -> mo } 
   </#>
  yields Date(day, mo);

fun dateToXml((Date(d,m))) { <em>{intToXml(d)}/{intToXml(m)}</em> }

sig travelForm : Formlet(BookingInfo)
var travelForm =
  formlet
    <table>
     <tr>
      <td>Person:</td> <td> { input -> person } </td>
     </tr>
     <tr>
      <td>Age:</td> <td> { inputInt -> age } </td>
     </tr>
     <tr>
      <td> Arrival:</td> <td> { date -> arr } </td>
     </tr>
     <tr>
      <td> Departure:</td> <td> { date -> dep }</td>
     </tr>
     <tr><td>{ submit("Submit") }</td></tr>
    </table>   
  yields 
    (person=person, age=age, arrival=arr, departure=dep);

fun showBookingInformation((person=p, age=a, arrival=arr, departure=dep)) {
 page
  <html>
   <h1>Results</h1>
   <p>
     You are {stringToXml(p)},  {intToXml(a)} years old.<br/>
     You'll arrive on {dateToXml(arr)}
     and leave on {dateToXml(dep)}.
   </p>
  </html>
}

page
 <html>
  <h1>Date:</h1>
  {travelForm => showBookingInformation}
 </html>
