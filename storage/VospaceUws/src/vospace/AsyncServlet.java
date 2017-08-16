package vospace;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import uws.UWSException;
import uws.job.ErrorType;
import uws.job.JobList;
import uws.job.JobThread;
import uws.job.UWSJob;
import uws.job.parameters.InputParamController;
import uws.job.user.JobOwner;
import uws.service.UWSServlet;
import uws.service.UWSUrl;

public class AsyncServlet extends UWSServlet {
	private static final long serialVersionUID = 1L;

	@Override
	public void initUWS() throws UWSException{
		addJobList(new JobList("trans"));
		addExpectedAdditionalParameter("time");
		addExpectedAdditionalParameter("direction");
		addExpectedAdditionalParameter("target");
		addExpectedAdditionalParameter("securitymethod");
		setInputParamController("time", new InputParamController(){
			@Override
			public Object getDefault(){
				return 10;
			}

			@Override
			public Object check(Object val) throws UWSException{
				int time;
				if (val instanceof Integer)
					time = ((Integer)val).intValue();
				else if (val instanceof String){
					try{
						time = Integer.parseInt((String)val);
					}catch(NumberFormatException nfe){
						throw new UWSException(UWSException.BAD_REQUEST, nfe, "Wrong \"time\" syntax: a positive integer is expected!", ErrorType.FATAL);
					}
				}else
					throw new UWSException(UWSException.BAD_REQUEST, "Wrong \"time\" type: a positive integer is expected!");

				if (time <= 0)
					throw new UWSException("Wrong \"time\" value: \"" + time + "\"! A positive integer is expected.");
				else
					return time;
			}

			@Override
			public boolean allowModification(){
				return true;
			}
		});
		setInputParamController("target", new InputParamController(){
			@Override
			public Object getDefault(){
				return "None";
			}

			@Override
			public boolean allowModification() {
				return false;
			}

			@Override
			public Object check(Object val) throws UWSException {
				String target;
				if (val instanceof String) {
					target = ((String)val).toString();
				}
				else {
					throw new UWSException(UWSException.BAD_REQUEST, "Wrong \"target\" type: a string is expected!");
				}
				return target;
			}
		});
		setInputParamController("direction", new InputParamController(){
			@Override
			public Object getDefault(){
				return "None";
			}

			@Override
			public boolean allowModification() {
				return false;
			}

			@Override
			public Object check(Object val) throws UWSException {
				String target;
				if (val instanceof String) {
					target = ((String)val).toString();
				}
				else {
					throw new UWSException(UWSException.BAD_REQUEST, "Wrong \"target\" type: a string is expected!");
				}
				return target;
			}
		});
		setInputParamController("securitymethod", new InputParamController(){
			@Override
			public Object getDefault(){
				return "None";
			}

			@Override
			public boolean allowModification() {
				return false;
			}

			@Override
			public Object check(Object val) throws UWSException {
				String target;
				if (val instanceof String) {
					target = ((String)val).toString();
				}
				else {
					throw new UWSException(UWSException.BAD_REQUEST, "Wrong \"target\" type: a string is expected!");
				}
				return target;
			}
		});
	}

	@Override
	public JobThread createJobThread(UWSJob job) throws UWSException{
		/*if (job.getJobList().getName().equals("PullFromVoSpace"))
			return new PullFromVoSpace(job);*/
		if (job.getParameter("direction").equals("PullFromVoSpace"))
			return new PullFromVoSpace(job);
		/*else if (job.getJobList().getName().equals("PushToVoSpace"))
			return new PushToVoSpace(job);*/
		else
			throw new UWSException("Impossible to create a job inside the jobs list \"" + job.getJobList().getName() + "\" !");
	}
	
	/*@Override
	protected void writeHomePage(UWSUrl requestUrl, HttpServletRequest req, HttpServletResponse resp, JobOwner user) throws UWSException, ServletException, IOException{
		PrintWriter out = resp.getWriter();

		out.println("<html><head><title>UWS4 example (using UWSServlet)</title></head><body>");
		out.println("<h1>UWS v4 Example (using UWSServlet)</h1");
		out.println("<p>Hello, this is an example of a use of the library UWS v4.1 !</p>");
		out.println("<p>Below is the list of all available jobs lists:</p>");

		out.println("<ul>");
		for(JobList jl : this){
			out.println("<li>" + jl.getName() + " - " + jl.getNbJobs() + " jobs - <a href=\"" + requestUrl.listJobs(jl.getName()) + "\">" + requestUrl.listJobs(jl.getName()) + "</a></li>");
		}
		out.println("</ul>");
	}*/


}
